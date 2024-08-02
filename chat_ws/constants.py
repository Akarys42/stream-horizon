import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", None) is not None

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")
if not ACCESS_TOKEN:
    raise ValueError("ACCESS_TOKEN is not set")

PORT = int(os.getenv("PORT", 23930))
