from dotenv import load_dotenv
import os

load_dotenv()

SERVER_ID = int(os.environ.get("SERVER_ID"))
DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")
TOKEN = os.environ.get("TOKEN")

ROLE_FOR_NEW_MEMBER = "new-member"
WELCOME_SURVEY_ID = 1
