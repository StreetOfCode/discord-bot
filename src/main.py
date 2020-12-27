import discord
import db

from discord.ext import commands

from config import TOKEN
from welcome import welcome_member, add_reaction_on_answer, remove_reaction_on_answer
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

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

    if message.content.startswith("/welcome"):
        await welcome_member(client, message.author)

    if message.content.startswith("$test"):
        db.add_test(message.content.split(" ")[1])


@client.event
async def on_member_join(member):
    print("Recognised that a member called " + member.name + " joined")
    await welcome_member(client, member)


@client.event
async def on_raw_reaction_add(payload):
    guild = get_server(client)
    if payload.member.id != guild.me.id:
        # If reaction is on welcome survey question (maybe first check if reaction is in correct channel)
        if (question_id := db.get_survey_question_id(payload.message_id)) is not None:
            channel = await client.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await add_reaction_on_answer(client=client, member=payload.member, question_id=question_id[0], emoji=payload.emoji, message=message)

@client.event
async def on_raw_reaction_remove(payload):
    guild = get_server(client)
    if payload.user_id != guild.me.id:
        # If reaction is on welcome survey question
        if (question_id := db.get_survey_question_id(payload.message_id)) is not None:
            await remove_reaction_on_answer(user_id=payload.user_id, question_id=question_id[0], emoji=payload.emoji)


client.run(TOKEN)
