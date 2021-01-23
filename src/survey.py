import logging

import discord

import db
from db.columns import (
    COLUMN_ID,
    COLUMN_SURVEY_ANSWER_EMOJI,
    COLUMN_SURVEY_ANSWER_TEXT,
    COLUMN_SURVEY_QUESTION_ORDER,
    COLUMN_SURVEY_QUESTION_TEXT,
    COLUMN_SURVEY_QUESTION_IS_MULTIPLE_CHOICE,
)
from log_utils import member_to_string
from utils import get_role

MULTIPLE_CHOICE_EMBED_DESCRIPTION = " Môžeš zvoliť viacero odpovedí!"
SURVEY_FINISHED_MESSAGE = "Koniec dotazníka. Ďakujeme pekne 🙂"
UNANSWERED_QUESTIONS_TEXT = "Ešte si neodpovedal/a na niektoré otázky, tak prosím odpovedz a potom znova klikni, že si odpovedal/a na všetky otázky. Otázky, na ktoré si neodpovedal/a:"


async def send_next_question(channel, member, survey_id, answered_question_id=None):
    logging.info(f"Sending next question to {member_to_string(member)}.")

    question, answers = db.get_next_survey_question(member.id, survey_id)
    if question is None or answers is None:
        logging.info(f"Question ({question} or answers ({answers}) are null.")
        return

    if not _should_send_next_question(
        question[COLUMN_SURVEY_QUESTION_ORDER], answered_question_id
    ):
        logging.info(f"Not sending next question.")
        return

    is_multiple_choice_question = question[COLUMN_SURVEY_QUESTION_IS_MULTIPLE_CHOICE]
    description = (
        MULTIPLE_CHOICE_EMBED_DESCRIPTION if is_multiple_choice_question else ""
    )

    question_embed = discord.Embed(
        title=question[COLUMN_SURVEY_QUESTION_TEXT],
        description=description,
        colour=discord.Colour(0xFFFF00),
    )

    for answer in answers:
        question_embed.add_field(
            name=answer[COLUMN_SURVEY_ANSWER_TEXT],
            value=answer[COLUMN_SURVEY_ANSWER_EMOJI],
            inline=True,
        )

    message = await channel.send(embed=question_embed)

    db.add_sent_survey_question(member.id, question[COLUMN_ID], message.id)

    for answer in answers:
        await message.add_reaction(emoji=answer[COLUMN_SURVEY_ANSWER_EMOJI])

    logging.info(
        f"Sent next question ({question[COLUMN_ID]}) to {member_to_string(member)}."
    )


def _should_send_next_question(next_question_order, answered_question_id):
    if answered_question_id is not None:
        previous_question_order = db.get_survey_question_order_or_none(
            answered_question_id
        )
        if (
            previous_question_order is not None
            and previous_question_order + 1 != next_question_order
        ):
            logging.info(f"Last answered question isn't the last question sent.")
            return False

    return True


async def remove_reaction_on_survey_answer(user_id, survey_id, question_id, emoji):
    logging.info(
        f"Removing reaction ({emoji}) from user ({user_id}) for survey ({survey_id}) question ({question_id})."
    )

    if db.is_survey_progress_finished(survey_id, user_id):
        logging.info(
            f"User ({user_id}) survey ({survey_id}) already finished. Keeping reaction in DB."
        )
        # Sadly, there is nothing we can do to set the reaction again in the UI.
        # We simply ignore the removal so it at least stays in our db.
        return

    # TODO maybe improve with single query?
    answer_id = db.get_answer_id(question_id, emoji)
    db.remove_user_answer(user_id, question_id, answer_id)
    logging.info(
        f"Removed reaction ({emoji}) from user ({user_id}) for survey ({survey_id}) question ({question_id})."
    )


async def add_reaction_on_survey_answer(
    client, member, survey_id, question_id, emoji, message
):
    logging.info(
        f"Adding reaction ({emoji}) from user {member_to_string(member)} for survey ({survey_id}) question ({question_id})."
    )

    if db.is_survey_progress_finished(survey_id, member.id):
        logging.info(
            f"User {member_to_string(member)} survey ({survey_id}) already finished. Removing reaction from message."
        )
        await message.remove_reaction(emoji, member)
        return

    existing_answer_to_question = db.get_answer_of_answered_survey_question_or_none(
        question_id, member.id
    )
    if (
        not db.is_multiple_choice_survey_question(question_id)
        and existing_answer_to_question is not None
    ):
        logging.info(
            f"Removing existing answer from user {member_to_string(member)} for survey ({survey_id}) question ({question_id})."
        )
        # Remove answer from db
        db.remove_user_answer(member.id, question_id, existing_answer_to_question)
        # Remove reaction from answer
        emoji_to_delete = db.get_emoji_from_survey_answer(existing_answer_to_question)
        await message.remove_reaction(emoji_to_delete, member)

    db.add_answer(member.id, question_id, db.get_answer_id(question_id, emoji))

    if db.are_all_survey_questions_answered(member.id, survey_id):
        logging.info(
            f"User {member_to_string(member)} answered all survey ({survey_id}) questions."
        )

        await add_receive_role_if_exists(client, member, survey_id)

        db.finish_user_survey_progress(survey_id, member.id)

        logging.info(f"User {member_to_string(member)} finished survey ({survey_id}).")

        await message.channel.send(SURVEY_FINISHED_MESSAGE)
    elif db.is_last_question(survey_id, question_id):
        logging.info(
            f"Sending unanswered questions to user {member_to_string(member)} on survey ({survey_id})."
        )
        await message.remove_reaction(emoji, member)

        unanswered_questions = db.get_unanswered_question_texts(survey_id, member.id)

        embed_description = "\n".join(
            ["- " + question for question in unanswered_questions]
        )
        embed = discord.Embed(
            title=UNANSWERED_QUESTIONS_TEXT,
            description=embed_description,
            colour=discord.Colour(0xFFFF00),
        )
        await message.channel.send(embed=embed)
    elif existing_answer_to_question is None:
        await send_next_question(message.channel, member, survey_id, question_id)


# Add receive role if survey contains receive_role_after_finish
async def add_receive_role_if_exists(client, member, survey_id):
    if (receive_role := db.get_survey_receive_role_or_none(survey_id)) is not None:
        survey_receive_role = get_role(client, receive_role)
        logging.info(
            f"Adding role ({survey_receive_role.name}) to user {member_to_string(member)}"
        )
        await member.add_roles(survey_receive_role)
