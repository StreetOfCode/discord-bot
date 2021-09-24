import logging

import discord

from log_utils import member_to_string

ALLOW_VIEW_CHANNEL = True
ALLOW_ADD_REACTIONS = False


async def create_channel(guild, member, channel_name):
    """
    Create channel which can be seen only by this member, bot and admins
    """
    logging.info(f"Creating channel {channel_name} for {member_to_string(member)}.")
    channel = await guild.create_text_channel(
        channel_name,
        overwrites={
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(
                view_channel=ALLOW_VIEW_CHANNEL,
                add_reactions=ALLOW_ADD_REACTIONS,
                send_messages=False,
            ),
            guild.me: discord.PermissionOverwrite(administrator=True),
        },
    )
    logging.info(f"Created channel {channel_name} for {member_to_string(member)}.")
    return channel


async def allow_sending_messages(channel, member):
    logging.info(
        f"Allowing message sending for {channel.name} for user {member_to_string(member)}."
    )
    await channel.set_permissions(
        member,
        view_channel=ALLOW_VIEW_CHANNEL,
        add_reactions=ALLOW_ADD_REACTIONS,
        send_messages=True,
    )


async def forbid_sending_messages(channel, member):
    logging.info(
        f"Forbidding message sending for {channel.name} for user {member_to_string(member)}."
    )
    await channel.set_permissions(
        member,
        view_channel=ALLOW_VIEW_CHANNEL,
        add_reactions=ALLOW_ADD_REACTIONS,
        send_messages=False,
    )
