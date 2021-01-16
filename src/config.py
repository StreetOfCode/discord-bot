import os

from dotenv import load_dotenv

load_dotenv()

SERVER_ID = int(os.environ.get("SERVER_ID"))
DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")
TOKEN = os.environ.get("TOKEN")
ADMIN_ROLE = os.environ.get("ADMIN_ROLE")
WELCOME_SURVEY_ID = int(os.environ.get("WELCOME_SURVEY_ID"))
PING_UNANSWERED_SURVEY_OLDER_THAN = os.environ.get("PING_UNANSWERED_SURVEY_OLDER_THAN")
DELETE_FINISHED_SURVEYS_OLDER_THAN = os.environ.get(
    "DELETE_FINISHED_SURVEYS_OLDER_THAN"
)
