import discord
import db

from utils import get_server, get_channel
from config import TEST_CHANNEL_ID


async def create_welcome_channel(guild, member):
    return await guild.create_text_channel(
        f"vitaj {member.display_name}",
        overwrites={
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(view_channel=True, add_reactions=True),
            guild.me: discord.PermissionOverwrite(administrator=True),
        },
    )


async def send_welcome_message(channel, member):
    embed = discord.Embed(
        title=f"Vitaj {member.display_name}",
        colour=discord.Colour(0xFFFF00),
        description=(
            """
:wave: Pred tym nez ta pustime do nasho Discordu, tak nam pls odpovedaj na zopar otazok. Staci ked na spravy pridas reakciu. Ked odpovies na vsetky otazky, tak ta pustime do nasho serveru.

**Alebo ak nechces odpovedat, tak proste pridaj :stop_button: na tuto spravu.**
"""
        ),
    )

    message = await channel.send(embed=embed)

    await message.add_reaction(emoji="⏹️")


async def welcome_member(client, member):
    # guild = get_server(client)
    # channel = await create_welcome_channel(guild, member)
    channel = get_channel(client, TEST_CHANNEL_ID)
    await send_welcome_message(channel, member)

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


async def remove_reaction_on_answer(user_id, question_id, emoji):
    answer_id = db.get_answer_id(question_id, emoji)
    db.remove_user_answer(user_id, question_id, answer_id)


async def add_reaction_on_answer(client, member, question_id, emoji, message):
    answer_id = db.get_answer_id(question_id, emoji)

    # Check if user already answered this question
    if (already_answer_id := db.get_answer_of_answered_survey_question(question_id, member.id)) is not None:
        # Remove answer from db
        db.remove_user_answer(member.id, question_id, already_answer_id[0])
        # Remove reaction from answer
        emoji_to_delete = db.get_emoji_from_survey_answer(already_answer_id[0])
        await message.remove_reaction(emoji_to_delete, member)

    db.add_answer(member.id, question_id, answer_id)

    if db.are_all_survey_questions_answered(member.id):
        # TODO: user answered all questions, set user's roles
        channel = get_channel(client, TEST_CHANNEL_ID)
        await channel.send("Odpovedal si na vsetko. Topka!")
