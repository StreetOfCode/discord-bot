import logging

import db
import survey
import survey_status
from channel import create_channel
from config import WELCOME_SURVEY_ID
from log_utils import member_to_string
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

    channel = await create_channel(
        get_server(client), member, f"vitaj {member.display_name}"
    )

    intro_message = db.get_survey_intro_message(WELCOME_SURVEY_ID)
    await survey.send_welcome_message(channel, member, intro_message)

    db.create_user_survey_progress(WELCOME_SURVEY_ID, member.id, channel.id)
    await survey.send_next_question(channel, member, WELCOME_SURVEY_ID)
