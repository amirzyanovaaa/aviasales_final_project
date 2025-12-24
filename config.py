import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")
AMADEUS_BASE_URL = os.getenv("AMADEUS_BASE_URL", "https://test.api.amadeus.com")
DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "RUB")
DB_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///db.sqlite3")
