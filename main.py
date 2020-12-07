import discord
from discord.ext import commands

client = discord.Client()

intents = discord.Intents.default()
intents.members = True
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


client.run("Nzg1MjAwMTcwNjI2NDQ5NDM4.X80YpA.z1ZPcTMQXyWbukBTO6ZD6Kt9x1o")
