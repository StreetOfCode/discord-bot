import logging
import db
from utils import get_server, is_admin
from config import WELCOME_SURVEY_ID, PING_UNANSWERED_SURVEY_OLDER_THAN
from welcome import welcome_member

PING_UNANSWERED_SURVEY_MESSAGE = "Čauko, iba pripomínam, že čakám na tvoje odpovede :)"


async def send_welcome_survey(client, context):
    """
    Only member with admin role can run this command
    Command sends welcome survey to all users who hasn't started survey and don't have admin role
    """
    logging.info("Executing send-welcome-survey command.")

    sent_to = []
    if is_admin(context.author):
        users_who_started_survey = db.get_all_user_ids_from_survey_progress(
            WELCOME_SURVEY_ID
        )
        for member in get_server(client).members:
            if member != client.user and member.id not in users_who_started_survey:
                if not is_admin(member):
                    await welcome_member(client, member)
                    sent_to.append(member.display_name)
        await context.channel.send(f"Sent to {sent_to}")
    else:
        logging.error(
            f"Unauthorized member {context.author} called send-welcome-survey command"
        )


async def ping_users_with_unanswered_questions(client, context):
    """
    Only member with admin role can run this command
    Command pings all users who have started welcome_survey (before interval) but haven't answered any questions
    """
    logging.info("Executing ping-unanswered-survey.")

    pinged = []
    if is_admin(context.author):
        users_from = db.get_all_in_progress_users_with_channel_from_survey_progress_created_older_than(
            WELCOME_SURVEY_ID, PING_UNANSWERED_SURVEY_OLDER_THAN
        )
        if len(users_from) > 0:
            users_with_no_answers = db.get_all_users_with_no_answer(
                WELCOME_SURVEY_ID, users_from.keys()
            )
            for user in users_with_no_answers:
                channel = client.get_channel(users_from[user])
                await channel.send(PING_UNANSWERED_SURVEY_MESSAGE)
                pinged.append(user)
        await context.channel.send(f"Pinged {len(pinged)} users")
    else:
        logging.error(
            f"Unauthorized member {context.author} called ping-unanswered-survey command"
        )
