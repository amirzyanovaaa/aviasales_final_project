from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from services.client import Client

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
amadeus_client = Client()