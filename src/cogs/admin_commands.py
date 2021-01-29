import logging
import random

import discord.utils
from discord.ext import commands

import db as db
import teams as teams
from config import (
    ADMIN_ROLE_ID,
    DELETE_FINISHED_SURVEYS_OLDER_THAN,
    PING_UNANSWERED_SURVEY_OLDER_THAN,
    WELCOME_SURVEY_ID,
)
from utils import get_server
from welcome import welcome_member

PING_UNANSWERED_SURVEY_MESSAGE = "Čauko, iba pripomínam, že čakám na tvoje odpovede :)"
TEAMS_EMBED_TITLE = "Vytvorené tímy"
CHANNEL_NOT_FOUND_ERROR_MESSAGE = "Zadaný channel som nenašiel!"


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="send-welcome-survey")
    @commands.has_role(ADMIN_ROLE_ID)
    async def send_welcome_survey(self, ctx):
        """
        Only member with admin role can run this command
        Command sends welcome survey to all users who hasn't started survey and don't have admin role
        """
        sent_to = []
        logging.info("Executing send-welcome-survey command.")
        users_who_started_survey = db.get_all_user_ids_from_survey_progress(
            WELCOME_SURVEY_ID
        )
        for member in get_server(self.bot).members:
            if member != self.bot.user and member.id not in users_who_started_survey:
                if discord.utils.get(member.roles, id=ADMIN_ROLE_ID) is None:
                    await welcome_member(self.bot, member)
                    sent_to.append(member.display_name)
        await ctx.channel.send(f"Sent to {sent_to}")

    @commands.command(name="ping-unanswered-survey")
    @commands.has_role(ADMIN_ROLE_ID)
    async def ping_users_with_unanswered_questions(self, ctx):
        """
        Only member with admin role can run this command
        Command pings all users who have started welcome_survey (before interval) but haven't answered any questions
        """
        pinged = []
        logging.info(
            f"Executing ping-unanswered-survey. OLDER_THAN is set to {PING_UNANSWERED_SURVEY_OLDER_THAN}"
        )
        users_from = db.get_all_in_progress_users_with_channel_from_survey_progress_created_older_than(
            WELCOME_SURVEY_ID, PING_UNANSWERED_SURVEY_OLDER_THAN
        )
        if len(users_from) > 0:
            for user, user_channel in users_from.items():
                channel = self.bot.get_channel(user_channel)
                await channel.send(PING_UNANSWERED_SURVEY_MESSAGE)
                pinged.append(user)
        await ctx.channel.send(f"Pinged {len(pinged)} users: {pinged}")

    @commands.command(name="delete-finished-surveys-channels")
    @commands.has_role(ADMIN_ROLE_ID)
    async def delete_finished_surveys_channels(self, ctx):
        """
        Only member with admin role can run this command
        Command deletes channel of surveys which have been completed before DELETE_SURVEYS_OLDER_THAN
        """
        deleted_channels = []
        logging.info(
            f"Executing delete_finished_surveys_channels command. OLDER_THAN is set to {DELETE_FINISHED_SURVEYS_OLDER_THAN}"
        )
        finished_surveys_channel_ids = db.get_completed_survey_channel_ids_older_than(
            DELETE_FINISHED_SURVEYS_OLDER_THAN
        )
        for channel_id in finished_surveys_channel_ids:
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                logging.info(
                    f"Channel ({channel_id}) not found on server but is in finished_surveys_channel_ids."
                )
                continue

            logging.info(f"Deleting channel ({channel_id}).")
            await channel.delete()
            db.set_user_survey_progress_status_to_channel_deleted(channel_id)
            deleted_channels.append(channel_id)

        await ctx.channel.send(f"Deleted {len(deleted_channels)} channels.")

    @commands.command(name="create-channel-teams")
    @commands.has_role(ADMIN_ROLE_ID)
    async def create_channel_teams(self, ctx, channel_id, number_of_teams=2):
        logging.info(
            f"Executing create-channel-teams command. Channel ID: {channel_id}. Number of teams: {number_of_teams}."
        )

        channel = self.bot.get_channel(int(channel_id))
        if channel is None:
            logging.info(f"Channel ({channel_id}) not found.")
            await ctx.channel.send(CHANNEL_NOT_FOUND_ERROR_MESSAGE)
            return

        member_names = [member.display_name for member in channel.members]

        created_teams = teams.create(member_names, number_of_teams, random.shuffle)

        teams_embed = discord.Embed(
            title=TEAMS_EMBED_TITLE,
            colour=discord.Colour(0xFFFF00),
        )
        for i, team in enumerate(created_teams):
            if len(team) == 0:
                continue

            team_name = f"Team {i + 1}"
            team_members_string = "\n".join(team)

            teams_embed.add_field(
                name=team_name, value=team_members_string, inline=True
            )

        await ctx.channel.send(embed=teams_embed)
