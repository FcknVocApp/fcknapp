from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "FCKN APP")
DEBUG = os.getenv("DEBUG", "False") == "True"
USERNAME = os.getenv("USERNAME", "admin")
TOX_LEVEL = os.getenv("TOX_LEVEL", "medium").lower()  # sensitive | medium | hardcore
