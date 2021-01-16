import logging

import discord
from discord.ext import commands

import admin_commands
import db
from config import TOKEN
from survey import add_reaction_on_survey_answer, remove_reaction_on_survey_answer
from utils import get_server
from welcome import welcome_member

logging.basicConfig(
    format="%(asctime)s - %(levelname)s: %(message)s", level=logging.INFO
)

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="/", intents=intents)


@client.command(name="send-welcome-survey")
async def send_welcome_survey_command(context):
    await admin_commands.send_welcome_survey(client, context)


@client.command(name="ping-unanswered-survey")
async def ping_unanswered_survey_command(context):
    await admin_commands.ping_users_with_unanswered_questions(client, context)


@client.command(name="delete-finished-surveys-channels")
async def delete_finished_surveys_channels(context):
    await admin_commands.delete_finished_surveys_channels(client, context)


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
                await add_reaction_on_survey_answer(
                    client=client,
                    member=payload.member,
                    survey_id=survey_id,
                    question_id=question_id,
                    emoji=payload.emoji,
                    message=message,
                )


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


client.run(TOKEN)
