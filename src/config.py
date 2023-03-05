from os import getenv
from dotenv import load_dotenv


load_dotenv()

DEBUG = getenv("DEBUG")
APP_SECRET = getenv("APP_SECRET")
DB_URL = getenv("DB_URL")
CLIENT_HOST_URL = getenv("CLIENT_HOST_URL")
REDIS_HOST_URL = getenv("REDIS_HOST_URL")
COOKIE_DOMAIN = getenv('COOKIE_DOMAIN')