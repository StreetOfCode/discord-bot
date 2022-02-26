import logging
import random

import discord.utils
from discord.ext import commands

import db as db
import survey_status
import teams as teams
from channel import create_channel
from config import (
    ADMINISTRATOR_ROLE_ID,
    DELETE_FINISHED_SURVEYS_OLDER_THAN,
    DELETE_UNANSWERED_SURVEYS_OLDER_THAN,
    PING_UNANSWERED_SURVEY_OLDER_THAN,
    WELCOME_SURVEY_ID,
)
from survey import send_next_question, send_welcome_message
from utils import get_member, get_server
from welcome import welcome_member

PING_UNANSWERED_SURVEY_MESSAGE = "Čauko, iba pripomínam, že čakám na tvoje odpovede :)"
TEAMS_EMBED_TITLE = "Vytvorené tímy"
CHANNEL_NOT_FOUND_ERROR_MESSAGE = "Zadaný channel som nenašiel!"


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="send-welcome-survey")
    @commands.has_role(ADMINISTRATOR_ROLE_ID)
    async def send_welcome_survey(self, ctx):
        """
        Only member with admin role can run this command.
        Command sends welcome survey to all users who hasn't started survey and don't have admin role
        """
        sent_to = []
        logging.info("Executing send-welcome-survey command.")
        users_who_started_survey = db.get_all_user_ids_from_survey_progress(
            WELCOME_SURVEY_ID
        )
        for member in get_server(self.bot).members:
            if member != self.bot.user and member.id not in users_who_started_survey:
                if discord.utils.get(member.roles, id=ADMINISTRATOR_ROLE_ID) is None:
                    await welcome_member(self.bot, member)
                    sent_to.append(member.display_name)
        await ctx.channel.send(f"Sent to {sent_to}")

    @commands.command(name="ping-unanswered-survey")
    @commands.has_role(ADMINISTRATOR_ROLE_ID)
    async def ping_users_with_unanswered_questions(self, ctx):
        """
        Only member with admin role can run this command.
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
    @commands.has_role(ADMINISTRATOR_ROLE_ID)
    async def delete_finished_surveys_channels(self, ctx):
        """
        Only member with admin role can run this command.
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
            db.set_user_survey_progress_status(
                channel_id, survey_status.FINISHED_CHANNEL_DELETED
            )
            deleted_channels.append(channel_id)

        await ctx.channel.send(f"Deleted {len(deleted_channels)} channels.")

    @commands.command(name="delete-unanswered-surveys-channels")
    @commands.has_role(ADMINISTRATOR_ROLE_ID)
    async def delete_unanswered_surveys_channels(self, ctx):
        """
        Only member with admin role can run this command.
        Command deletes channel of surveys which have been unanswered longer than DELETE_UNANSWERED_SURVEYS_OLDER_THAN
        """
        deleted_channels = []
        logging.info(
            f"Executing delete_unanswered_surveys_channels command. OLDER_THAN is set to {DELETE_UNANSWERED_SURVEYS_OLDER_THAN}"
        )
        unanswered_channel_ids = db.get_in_progress_survey_channel_ids_older_than(
            DELETE_UNANSWERED_SURVEYS_OLDER_THAN
        )
        for channel_id in unanswered_channel_ids:
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                logging.info(
                    f"Channel ({channel_id}) not found on server but is in survey progress."
                )
                continue

            logging.info(f"Deleting channel ({channel_id}).")
            await channel.delete()
            db.set_user_survey_progress_status(
                channel_id, survey_status.UNANSWERED_CHANNEL_DELETED
            )
            deleted_channels.append(channel_id)

        await ctx.channel.send(f"Deleted {len(deleted_channels)} channels.")

    @commands.command(name="create-channel-teams")
    @commands.has_role(ADMINISTRATOR_ROLE_ID)
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

    @commands.command(name="send-survey")
    @commands.has_role(ADMINISTRATOR_ROLE_ID)
    async def send_survey(self, ctx, survey_id):
        """
        Only member with admin role can run this command.
        Command sends survey (id of survey in first parameter) to all users who are survey-fans
        (They answered in welcome quiz that they are ok with sending more surveys)
        """

        logging.info(f"Executing send-survey command for survey_id {survey_id}")

        if db.check_survey_exists(survey_id):
            survey_fans = db.find_all_answer_alias_responders("survey-fan")
            users_who_started_survey = db.get_all_user_ids_from_survey_progress(
                survey_id
            )
            final_users_to_send_survey_to = list(
                set(survey_fans) - set(users_who_started_survey)
            )

            sent_to = []
            for user_id in final_users_to_send_survey_to:
                member = get_member(self.bot, user_id)
                if member is None:
                    # member does not longer exist
                    continue

                channel_name = f"{member.display_name}-{db.get_survey_channel_name_suffix(survey_id)}"
                channel = await create_channel(
                    get_server(self.bot), member, channel_name
                )

                intro_message = db.get_survey_intro_message(survey_id)
                await send_welcome_message(channel, member, intro_message)

                db.create_user_survey_progress(survey_id, member.id, channel.id)
                await send_next_question(channel, member, survey_id)

                sent_to.append(member.display_name)

            await ctx.channel.send(f"Sent to {sent_to}")

        else:
            logging.info(
                f"Calling send-survey command for survey_id {survey_id}, but this survey doesn't exist"
            )
            await ctx.channel.send(f"Survey with id {survey_id} wasn't found")

    @commands.command(name="clear-show-stats-cache")
    @commands.has_role(ADMINISTRATOR_ROLE_ID)
    async def clear_show_stats_cache(self, ctx):
        """
        Only member with admin role can run this command.
        Command deletes all rows from show_stats_cache db table
        """
        logging.info(f"Executing clear_show_stats_cache command")
        db.remove_all_show_stats_cache()
        await ctx.channel.send("Successfully cleared show_stats_cache")
