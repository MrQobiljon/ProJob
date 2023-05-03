from telebot import TeleBot
from telebot.types import BotCommand

from config import TOKEN
from database.database import Database

bot = TeleBot(TOKEN, parse_mode='html')
db = Database()


bot.set_my_commands(
    commands=[
        BotCommand('/start', 'Botni qayta ishga tushirish'),
    ]
)
