import discord
from discord.ext import commands

import db
from config import OLD_MEMBER_ROLE, TOKEN, WELCOME_SURVEY_ID
from utils import get_role, get_server, is_admin
from welcome import (
    add_reaction_on_survey_answer,
    remove_reaction_on_survey_answer,
    welcome_member,
)

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="/", intents=intents)


@client.command(name="send-welcome-survey")
async def send_welcome_survey_command(context):
    """
    Only member with admin role can run this command
    Command sends welcome survey to all users who hasn't started survey and don't have admin role
    Also it gives them old_member role
    """
    sent_to = []
    if is_admin(context.author):
        users_that_started_survey = db.get_all_user_ids_from_survey_progress(
            WELCOME_SURVEY_ID
        )
        old_member_role = get_role(client, OLD_MEMBER_ROLE)
        for member in get_server(client).members:
            if member != client.user and member.id not in users_that_started_survey:
                if not is_admin(member):
                    await member.add_roles(old_member_role)
                    await welcome_member(client, member)
                    sent_to.append(member.display_name)
        await context.channel.send(f"Sent to {sent_to}")
    else:
        print(
            f"Unauthorized member {context.author} called send-welcome-survey command"
        )


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

    await client.process_commands(message)


@client.event
async def on_member_join(member):
    print("Recognised that a member called " + member.name + " joined")
    await welcome_member(client, member)


@client.event
async def on_raw_reaction_add(payload):
    guild = get_server(client)
    if payload.member.id != guild.me.id:
        # If reaction is on welcome survey question
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
        # If reaction is on welcome survey question
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
