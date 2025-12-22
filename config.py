import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BOT_TOKEN = '8523459252:AAFPRYvniIoPWoSiLWv8jJaaTmwvv3Q5gwE'
AMADEUS_API_KEY = 'mYjjgWAsz3SptSG2JdK6CnvZYZRfQgJT'
AMADEUS_API_SECRET = 'sfj3n00vw6NHVvg0'
AMADEUS_BASE_URL = os.getenv("AMADEUS_BASE_URL", "https://test.api.amadeus.com")
DEFAULT_CURRENCY = "RUB"

DB_URL = "sqlite+aiosqlite:///db.sqlite3"

