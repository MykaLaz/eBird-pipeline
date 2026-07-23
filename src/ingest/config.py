import os
from dotenv import load_dotenv

load_dotenv()  # reads secrets from .env into os.environ object as a dict

EBIRD_API_KEY = os.environ[
    "EBIRD_API_KEY"
]  # raises KeyError loudly if missing — good, fail fast
EBIRD_BASE_URL = "https://api.ebird.org/v2"
