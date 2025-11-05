import os
from dotenv import load_dotenv
from app.utils.constants import MISSING_ENV_VARS_ERROR

# Load environment variables
load_dotenv(override=True)

# === Required API Keys and Tokens ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN")
POST_NICHE = os.getenv("POST_NICHE")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
DB_COLLECTION_NAME = os.getenv("DB_COLLECTION_NAME")

# === Check for missing environment variables ===
required_vars = [
    "OPENAI_API_KEY",
    "LINKEDIN_ACCESS_TOKEN",
    "LINKEDIN_PERSON_URN",
    "POST_NICHE",
    "GEMINI_API_KEY",
    "MONGO_URI",
    "DB_NAME",
    "DB_COLLECTION_NAME",
]

missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    # Format the message from constant.py
    error_message = MISSING_ENV_VARS_ERROR.format(vars=", ".join(missing_vars))
    raise EnvironmentError(error_message)
