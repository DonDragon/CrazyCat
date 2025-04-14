from aiogram import types
from config import ADMIN_IDS
from database import add_user, get_balance, add_bonus, use_bonus

async def start_handler(message: types.Message):
    add_user(message.from_user.id, message.from_user.username)
    await message.answer("Добро пожаловать! Ваш бонусный счёт создан.")

async def balance_handler(message: types.Message):
    balance = get_balance(message.from_user.id)
    await message.answer(f"Ваш текущий баланс: {balance} бонусов.")

async def add_bonus_handler(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.reply("У вас нет прав для этой команды.")

    parts = message.text.split()
    if len(parts) != 3:
        return await message.reply("Формат: /add_bonus <user_id> <кол-во>")

    user_id = int(parts[1])
    points = int(parts[2])
    add_bonus(user_id, points)
    await message.answer(f"{points} бонусов добавлено пользователю {user_id}")

async def use_bonus_handler(message: types.Message):
    parts = message.text.split()
    if len(parts) != 2:
        return await message.reply("Формат: /use_bonus <кол-во>")

    points = int(parts[1])
    current = get_balance(message.from_user.id)
    if current < points:
        return await message.reply("Недостаточно бонусов.")

    use_bonus(message.from_user.id, points)
    await message.answer(f"{points} бонусов списано. Остаток: {get_balance(message.from_user.id)}")
