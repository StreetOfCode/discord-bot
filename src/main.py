import discord
from discord.ext import commands

from config import TOKEN
from db import add_test
from welcome import welcome_member, on_answer
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
        add_test(message.content.split(" ")[1])


@client.event
async def on_member_join(member):
    print("Recognised that a member called " + member.name + " joined")
    await welcome_member(client, member)


@client.event
async def on_raw_reaction_add(payload):
    guild = get_server(client)
    if payload.member.id != guild.me.id:
        await on_answer(client, payload.member, payload.message_id, payload.emoji)


client.run(TOKEN)
