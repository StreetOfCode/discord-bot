import os

from dotenv import load_dotenv

load_dotenv()

SERVER_ID = int(os.environ.get("SERVER_ID"))
DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")
TOKEN = os.environ.get("TOKEN")
MEMBER_ROLE = os.environ.get("MEMBER_ROLE")
NEW_MEMBER_ROLE = os.environ.get("NEW_MEMBER_ROLE")
OLD_MEMBER_ROLE = os.environ.get("OLD_MEMBER_ROLE")
ADMIN_ROLE = os.environ.get("ADMIN_ROLE")
WELCOME_SURVEY_ID = int(os.environ.get("WELCOME_SURVEY_ID"))
