import logging

import discord

import db
import survey
import survey_status
from config import WELCOME_SURVEY_ID
from log_utils import channel_to_string, member_to_string
from utils import get_server


async def welcome_member(client, member):
    logging.info(f"Welcoming member {member_to_string(member)}.")

    welcome_survey_status = db.get_user_survey_progress_status_or_none(
        WELCOME_SURVEY_ID, member.id
    )
    if welcome_survey_status in [
        survey_status.FINISHED,
        survey_status.FINISHED_CHANNEL_DELETED,
    ]:
        logging.info(f"{member_to_string(member)} already finished welcome survey.")
        await survey.add_receive_role_if_exists(client, member, WELCOME_SURVEY_ID)
        return

    if welcome_survey_status == survey_status.IN_PROGRESS:
        logging.info(
            f"{member_to_string(member)} has already started survey once. Clearing old survey data."
        )
        db.clear_all_user_survey_progress(WELCOME_SURVEY_ID, member.id)

    channel = await _create_welcome_channel(get_server(client), member)

    intro_message = db.get_survey_intro_message(WELCOME_SURVEY_ID)
    await _send_welcome_message(channel, member, intro_message)

    db.create_user_survey_progress(WELCOME_SURVEY_ID, member.id, channel.id)
    await survey.send_next_question(channel, member, WELCOME_SURVEY_ID)


# Create channel which can be seen only by this member, bot and admins
async def _create_welcome_channel(guild, member):
    logging.info(f"Creating welcome channel for {member_to_string(member)}.")
    channel = await guild.create_text_channel(
        f"vitaj {member.display_name}",
        overwrites={
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(
                view_channel=True, add_reactions=False, send_messages=False
            ),
            guild.me: discord.PermissionOverwrite(administrator=True),
        },
    )
    logging.info(
        f"Created welcome channel {channel_to_string(channel)} for {member_to_string(member)}."
    )
    return channel


async def _send_welcome_message(channel, member, welcome_message):
    logging.info(
        f"Sending welcome message for {member_to_string(member)} to channel {channel_to_string(channel)}."
    )

    embed = discord.Embed(
        title=f"Vitaj {member.display_name}",
        colour=discord.Colour(0xFFFF00),
        description=welcome_message,
    )
    await channel.send(embed=embed)
