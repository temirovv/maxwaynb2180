from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database.db_api import Database

TOKEN = "8446233580:AAFzOvjbaZTBx036SdOSawd05vPVxBrQeuE"

dp = Dispatcher()
baza = Database('database/main.db')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
ADMIN = 1058730773
