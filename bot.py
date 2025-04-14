import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

from config import BOT_TOKEN
from handlers import start_handler, balance_handler, add_bonus_handler, use_bonus_handler

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def handle_start(message: Message):
    await start_handler(message)

@dp.message_handler(commands=["balance"])
async def handle_balance(message: Message):
    await balance_handler(message)

@dp.message_handler(commands=["add_bonus"])
async def handle_add_bonus(message: Message):
    await add_bonus_handler(message)

@dp.message_handler(commands=["use_bonus"])
async def handle_use_bonus(message: Message):
    await use_bonus_handler(message)

if __name__ == "__main__":
    from database import conn  # Ensure DB is initialized
    executor.start_polling(dp)

@dp.message_handler(lambda message: message.text == "💰 Мой баланс")
async def handle_text_balance(message: Message):
    await balance_handler(message)

@dp.message_handler(lambda message: message.text == "🎁 Использовать бонусы")
async def handle_text_use_bonus(message: Message):
    await message.answer("Введите команду /use_bonus <кол-во>, чтобы использовать бонусы.")
