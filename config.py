from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

BASE_URL = os.getenv("BASE_URL")
LOGIN_URL = f"{BASE_URL}oauth/authorize?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&response_type=code&view_private=read_all&approval_prompt=auto&scope=activity:read_all;profile:read_all"
ACCESS_TOKEN_ENDPOINT = f"{BASE_URL}oauth/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=authorization_code&code="
