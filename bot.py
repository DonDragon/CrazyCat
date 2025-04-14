import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from config import BOT_TOKEN, ADMIN_IDS
from database import init_db, add_user, get_balance, get_all_users, update_phone, add_bonus, use_bonus, get_user_by_phone

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# --- Клавиатура запроса номера ---
phone_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
phone_keyboard.add(KeyboardButton("📱 Отправить номер", request_contact=True))

# --- Кнопки для админ-панели ---
def admin_user_menu(user_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("➕ Начислить 10", callback_data=f"add:{user_id}"),
        types.InlineKeyboardButton("➖ Списать 10", callback_data=f"use:{user_id}")
    )
    return keyboard

@dp.message_handler(commands=["start"])
async def start_cmd(message: Message):
    add_user(message.from_user.id, message.from_user.username)
    await message.answer("Добро пожаловать! Пожалуйста, отправьте свой номер телефона:", reply_markup=phone_keyboard)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contact_handler(message: Message):
    if message.contact.user_id != message.from_user.id:
        return await message.answer("Пожалуйста, отправьте свой собственный номер.")
    update_phone(message.from_user.id, message.contact.phone_number)
    await message.answer("Номер сохранён. Вы можете проверить баланс: /balance")

@dp.message_handler(commands=["balance"])
async def balance_cmd(message: Message):
    balance = get_balance(message.from_user.id)
    await message.answer(f"Ваш текущий баланс: {balance} бонусов.")

@dp.message_handler(commands=["admin"])
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("У вас нет доступа.")
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("📋 Список пользователей"), KeyboardButton("🔍 Найти по номеру"))
    await message.answer("Выберите действие:", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text == "📋 Список пользователей")
async def user_list(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    users = get_all_users()
    if not users:
        return await message.answer("Список пользователей пуст.")
    
    keyboard = types.InlineKeyboardMarkup()
    for user_id, username, phone in users:
        label = f"{username or 'Без ника'} ({phone or 'без телефона'})"
        keyboard.add(types.InlineKeyboardButton(label, callback_data=f"select:{user_id}"))
    await message.answer("Выберите пользователя:", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text == "🔍 Найти по номеру")
async def request_phone_search(message: Message):
    await message.answer("Введите номер телефона пользователя (в формате +1234567890):")

@dp.message_handler(lambda msg: msg.text.startswith("+") and len(msg.text) >= 10)
async def search_by_phone(message: Message):
    result = get_user_by_phone(message.text.strip())
    if result:
        user_id = result[0]
        await message.answer(f"Пользователь найден: ID {user_id}", reply_markup=admin_user_menu(user_id))
    else:
        await message.answer("Пользователь с таким номером не найден.")

@dp.callback_query_handler(lambda c: c.data.startswith("select:"))
async def select_user(callback: CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    await callback.message.edit_text(f"Выбран пользователь ID {user_id}", reply_markup=admin_user_menu(user_id))

@dp.callback_query_handler(lambda c: c.data.startswith("add:"))
async def add_points(callback: CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    add_bonus(user_id, 10)
    await callback.message.answer(f"Начислено 10 бонусов пользователю {user_id}.")

@dp.callback_query_handler(lambda c: c.data.startswith("use:"))
async def remove_points(callback: CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    use_bonus(user_id, 10)
    await callback.message.answer(f"Списано 10 бонусов у пользователя {user_id}.")

if __name__ == "__main__":
    init_db()
    executor.start_polling(dp)
