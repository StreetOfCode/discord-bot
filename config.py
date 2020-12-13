from dotenv import load_dotenv
import os


load_dotenv()

SERVER_ID = os.environ.get("SERVER_ID")
WELCOME_CHANNEL_ID = os.environ.get("WELCOME_CHANNEL_ID")
TEST_MEMBER_ID = os.environ.get("TEST_MEMBER_ID")
DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")
TOKEN = os.environ.get("TOKEN")
