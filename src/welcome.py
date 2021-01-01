import discord
from discord.utils import get

import db
from config import MEMBER_ROLE, NEW_MEMBER_ROLE, WELCOME_SURVEY_ID
from utils import get_role, get_server

MULTIPLE_CHOICE_EMBED_DESCRIPTION = " Môžeš zvoliť viacero odpovedí!"


async def send_welcome_message(channel, member, welcome_message):
    embed = discord.Embed(
        title=f"Vitaj {member.display_name}",
        colour=discord.Colour(0xFFFF00),
        description=welcome_message,
    )
    await channel.send(embed=embed)


# Create channel which can be seen only by this member, bot and admins
async def create_welcome_channel(guild, member):
    channel = await guild.create_text_channel(
        f"vitaj {member.display_name}",
        overwrites={
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(
                view_channel=True, add_reactions=False, send_messages=False
            ),
            guild.me: discord.PermissionOverwrite(administrator=True),
        },
    )
    return channel


async def welcome_member(client, member):
    welcome_survey_status = db.get_user_survey_progress_status_or_none(
        WELCOME_SURVEY_ID, member.id
    )
    if welcome_survey_status == "FINISHED":
        member_role = get_role(client, MEMBER_ROLE)
        await member.add_roles(member_role)
        return

    if welcome_survey_status == "IN_PROGRESS":
        db.clear_all_user_survey_progress(WELCOME_SURVEY_ID, member.id)

    new_member_role = get_role(client, NEW_MEMBER_ROLE)
    await member.add_roles(new_member_role)

    channel = await create_welcome_channel(get_server(client), member)

    intro_message = db.get_survey_intro_message(WELCOME_SURVEY_ID)
    await send_welcome_message(channel, member, intro_message)

    db.create_user_survey_progress(WELCOME_SURVEY_ID, member.id, channel.id)
    await send_next_question(channel, member)


async def send_next_question(channel, member):
    question, answers = db.get_next_survey_question(member.id, WELCOME_SURVEY_ID)
    if question is None or answers is None:
        return

    is_multiple_choice_question = question[3]
    description = (
        MULTIPLE_CHOICE_EMBED_DESCRIPTION if is_multiple_choice_question else ""
    )

    position_embed = discord.Embed(
        title=question[2], description=description, colour=discord.Colour(0xFFFF00)
    )

    for (_, _, _, text, emoji, _) in answers:
        position_embed.add_field(name=text, value=emoji, inline=True)

    message = await channel.send(embed=position_embed)

    for (_, _, _, _, emoji, _) in answers:
        await message.add_reaction(emoji=emoji)

    db.add_sent_survey_question(member.id, question[0], message.id)


async def remove_reaction_on_survey_answer(user_id, survey_id, question_id, emoji):
    is_finished = db.is_survey_progress_finished(survey_id, user_id)
    if is_finished:
        # Sadly, there is nothing we can do to set the reaction again in the UI.
        # We simply ignore the removal so it at least stays in our db.
        return

    # TODO maybe improve with single query?
    answer_id = db.get_answer_id(question_id, emoji)
    db.remove_user_answer(user_id, question_id, answer_id)


async def add_reaction_on_survey_answer(
    client, member, survey_id, question_id, emoji, message
):
    is_finished = db.is_survey_progress_finished(survey_id, member.id)
    if is_finished:
        await message.remove_reaction(emoji, member)
        return

    answer_id = db.get_answer_id(question_id, emoji)

    is_multiple_choice_question = db.is_multiple_choice_survey_question(question_id)
    already_answer_id = db.get_answer_of_answered_survey_question_or_none(
        question_id, member.id
    )
    if not is_multiple_choice_question and already_answer_id is not None:
        # Remove answer from db
        db.remove_user_answer(member.id, question_id, already_answer_id)
        # Remove reaction from answer
        emoji_to_delete = db.get_emoji_from_survey_answer(already_answer_id)
        await message.remove_reaction(emoji_to_delete, member)

    db.add_answer(member.id, question_id, answer_id)

    if db.are_all_survey_questions_answered(member.id):
        # Add receive role if survey contains receive_role_after_finish
        if (receive_role := db.get_survey_receive_role_or_none(survey_id)) is not None:
            member_role = get(get_server(client).roles, name=receive_role)
            await member.add_roles(member_role)

        if survey_id == WELCOME_SURVEY_ID:
            new_member_role = get(get_server(client).roles, name=NEW_MEMBER_ROLE)
            await member.remove_roles(new_member_role)

        db.finish_user_survey_progress(survey_id, member.id)

        # TODO remove or something else
        await message.channel.send("Odpovedal si na vsetko. Topka!")
    elif db.is_last_question(survey_id, question_id):
        await message.remove_reaction(emoji, member)

        unanswered_questions = db.get_unanswered_question_texts(survey_id, member.id)

        embed_description = "\n".join(
            ["- " + question for question in unanswered_questions]
        )
        embed = discord.Embed(
            title="Ešte si neodpovedal/a na niektoré otázky:",
            description=embed_description,
            colour=discord.Colour(0xFFFF00),
        )
        await message.channel.send(embed=embed)
    elif already_answer_id is None:
        await send_next_question(message.channel, member)
