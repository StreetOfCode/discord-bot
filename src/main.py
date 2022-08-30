import logging
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

import cogs
import db
from config import TOKEN
from question import is_question_open_ended
from survey import add_survey_answer, remove_reaction_on_survey_answer
from utils import get_server
from welcome import welcome_member

logging.basicConfig(
    format="%(asctime)s - %(levelname)s: %(message)s", level=logging.INFO
)

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

client = commands.Bot(command_prefix="/", intents=intents)


async def main():
    _cogs = [
        cogs.admin_commands.AdminCommands(client),
        cogs.public_commands.PublicCommands(client),
    ]
    for cog in _cogs:
        await client.add_cog(cog)

    async with client:
        await client.start(TOKEN)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        # Don't log command not found everytime someone calls /whatever
        return
    raise error


@client.event
async def on_ready():
    logging.info("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)


@client.event
async def on_member_join(member):
    logging.info(f"{member.name} joined.")
    await welcome_member(client, member)


@client.event
async def on_raw_reaction_add(payload):
    guild = get_server(client)
    if payload.member.id != guild.me.id:
        if (
            survey_id := db.get_survey_id_from_user_survey_progress_or_none(
                payload.member.id, payload.channel_id
            )
        ) is not None:
            if (
                question_id := db.get_survey_question_id_or_none(payload.message_id)
            ) is not None:
                channel = await client.fetch_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                try:
                    await add_survey_answer(
                        client=client,
                        member=payload.member,
                        survey_id=survey_id,
                        question_id=question_id,
                        message=message,
                        is_open_ended=False,
                        emoji=payload.emoji,
                    )
                except ValueError as e:
                    logging.error(f"Error while adding survey answer. {e}")


@client.event
async def on_raw_reaction_remove(payload):
    guild = get_server(client)
    if payload.user_id != guild.me.id:
        if (
            survey_id := db.get_survey_id_from_user_survey_progress_or_none(
                payload.user_id, payload.channel_id
            )
        ) is not None:
            if (
                question_id := db.get_survey_question_id_or_none(payload.message_id)
            ) is not None:
                await remove_reaction_on_survey_answer(
                    user_id=payload.user_id,
                    survey_id=survey_id,
                    question_id=question_id,
                    emoji=payload.emoji,
                )


@client.event
async def on_message(message):
    guild = get_server(client)
    if message.author.id != guild.me.id:
        if (
            survey_id := db.get_survey_id_from_user_survey_progress_or_none(
                message.author.id, message.channel.id
            )
        ) is not None:
            logging.info(f"Received survey answer as a message.")
            question = db.get_current_survey_question_or_none(
                message.author.id, survey_id
            )
            logging.info(f"Current question: {question}.")
            if question is None:
                logging.info(f"Current question is null.")
                return

            if not is_question_open_ended(question):
                logging.info(
                    f"Received message in a survey channel with non-open-ended question."
                )
                return

            logging.info(f"Storing message '{message.content}' answer")
            try:
                await add_survey_answer(
                    client=client,
                    member=message.author,
                    survey_id=survey_id,
                    question_id=question[0],
                    message=message,
                    is_open_ended=True,
                    emoji=None,
                )
            except ValueError as e:
                logging.error(f"Error while adding survey answer. {e}")

            # don't process commands if answer was being submitted
            return

    await client.process_commands(message)


@client.event
async def on_message_edit(message_before, message_after):
    guild = get_server(client)
    if message_before.author.id != guild.me.id:
        if (
            survey_id := db.get_survey_id_from_user_survey_progress_or_none(
                message_before.author.id, message_before.channel.id
            )
        ) is not None:
            logging.info(f"Received a request to edit an open-ended question answer.")
            question_id = db.get_open_ended_question_id_from_answer_or_none(
                message_before.id
            )
            if question_id is None:
                logging.info(
                    f"Open-ended question not found for message ID: {message_before.id}."
                )
                return

            logging.info(
                f"Editing answer for question ID: {question_id}. Updating answer from '{message_before.content}' to '{message_after.content}'"
            )
            try:
                await add_survey_answer(
                    client=client,
                    member=message_after.author,
                    survey_id=survey_id,
                    question_id=question_id,
                    message=message_after,
                    is_open_ended=True,
                    emoji=None,
                )
            except ValueError as e:
                logging.error(f"Error while adding survey answer. {e}")


asyncio.run(main())
