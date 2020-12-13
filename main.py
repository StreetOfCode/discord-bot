import discord
from discord.ext import commands

from config import SERVER_ID, TEST_MEMBER_ID, TOKEN
from db import add_test


intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="/", intents=intents)


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    # await send_welcome_message(await get_member(TEST_MEMBER_ID))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

    if message.content.startswith("$test"):
        add_test(message.content.split(" ")[1])


@client.event
async def on_member_join(member):
    print("Recognised that a member called " + member.name + " joined")
    send_welcome_message(member)


async def send_welcome_message(member):
    guild = get_server()

    channel = await guild.create_text_channel(
        "introduction 2",
        overwrites={
            member: discord.PermissionOverwrite(view_channel=True, add_reactions=True),
            guild.me: discord.PermissionOverwrite(administrator=True),
        },
    )

    await channel.send("Welcome mah maaan!")


def get_member(id):
    guild = get_server()
    member = guild.get_member(id)
    return member


def get_server():
    return next(g for g in client.guilds if g.id == SERVER_ID)


client.run(TOKEN)
