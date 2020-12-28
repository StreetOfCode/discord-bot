import discord

import db

from discord.ext import commands

from config import TOKEN, ROLE_FOR_NEW_MEMBER
from welcome import welcome_member, add_reaction_on_survey_answer, remove_reaction_on_survey_answer
from utils import get_server

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="/", intents=intents)


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # TODO REMOVE
    if message.content.startswith("/welcome"):
        await welcome_member(client, message.author)


@client.event
async def on_member_join(member):
    print("Recognised that a member called " + member.name + " joined")
    new_member_role = discord.utils.get(get_server(client).roles, name=ROLE_FOR_NEW_MEMBER)
    await member.add_roles(new_member_role)
    await welcome_member(client, member)


@client.event
async def on_raw_reaction_add(payload):
    guild = get_server(client)
    if payload.member.id != guild.me.id:
        # If reaction is on welcome survey question
        if (survey_id := db.get_survey_id_from_user_survey_progress_or_none(payload.member.id, payload.channel_id)) is not None:
            if (question_id := db.get_survey_question_id_or_none(payload.message_id)) is not None:
                channel = await client.fetch_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                await add_reaction_on_survey_answer(client=client, member=payload.member, survey_id=survey_id, question_id=question_id, emoji=payload.emoji, message=message)


@client.event
async def on_raw_reaction_remove(payload):
    guild = get_server(client)
    if payload.user_id != guild.me.id:
        # If reaction is on welcome survey question
        if db.get_survey_id_from_user_survey_progress_or_none(payload.user_id, payload.channel_id) is not None:
            if (question_id := db.get_survey_question_id_or_none(payload.message_id)) is not None:
                await remove_reaction_on_survey_answer(user_id=payload.user_id, question_id=question_id, emoji=payload.emoji)


client.run(TOKEN)
