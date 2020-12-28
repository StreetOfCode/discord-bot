import discord
import db

from utils import get_server
from config import ROLE_FOR_NEW_MEMBER, WELCOME_SURVEY_ID

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
            member: discord.PermissionOverwrite(view_channel=True, add_reactions=True),
            guild.me: discord.PermissionOverwrite(administrator=True),
        },
    )
    return channel


async def welcome_member(client, member):
    channel = await create_welcome_channel(get_server(client), member)

    intro_message = db.get_survey_intro_message(WELCOME_SURVEY_ID)
    await send_welcome_message(channel, member, intro_message)

    db.create_user_survey_progress(WELCOME_SURVEY_ID, member.id, channel.id)

    questions = db.get_survey_questions()
    for question, answers in questions:
        position_embed = discord.Embed(
            title=question[2], colour=discord.Colour(0xFFFF00)
        )
        for (_, _, _, text, emoji) in answers:
            position_embed.add_field(name=text, value=emoji, inline=True)

        message = await channel.send(embed=position_embed)

        for (_, _, _, _, emoji) in answers:
            await message.add_reaction(emoji=emoji)

        db.add_sent_survey_question(member.id, question[0], message.id)


async def remove_reaction_on_survey_answer(user_id, question_id, emoji):
    # TODO maybe improve with single query?
    answer_id = db.get_answer_id(question_id, emoji)
    db.remove_user_answer(user_id, question_id, answer_id)


async def add_reaction_on_survey_answer(client, member, survey_id, question_id, emoji, message):
    answer_id = db.get_answer_id(question_id, emoji)

    # Check if user have already answered this question
    if (already_answer_id := db.get_answer_of_answered_survey_question_or_none(question_id, member.id)) is not None:
        # Remove answer from db
        db.remove_user_answer(member.id, question_id, already_answer_id)
        # Remove reaction from answer
        emoji_to_delete = db.get_emoji_from_survey_answer(already_answer_id)
        await message.remove_reaction(emoji_to_delete, member)

    db.add_answer(member.id, question_id, answer_id)

    if db.are_all_survey_questions_answered(member.id):
        # Add receive role if survey contains receive_role_after_finish
        if (receive_role := db.get_survey_receive_role_or_none(survey_id)) is not None:
            member_role = discord.utils.get(get_server(client).roles, name=receive_role)
            await member.add_roles(member_role)

        if survey_id == WELCOME_SURVEY_ID:
            new_member_role = discord.utils.get(get_server(client).roles, name=ROLE_FOR_NEW_MEMBER)
            await member.remove_roles(new_member_role)

        db.finish_user_survey_progress(survey_id, member.id)

        # TODO remove or something else
        await message.channel.send("Odpovedal si na vsetko. Topka!")
