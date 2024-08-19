import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
import sqlite3
from config import TOKEN
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import logging
from googletrans import Translator
import requests
import random

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

button_registr = KeyboardButton(text="Регистрация")
button_exchange_rates = KeyboardButton(text="Курсы валют")
button_tips = KeyboardButton(text="Советы по экономии")
button_finances = KeyboardButton(text="Финансы")

keyboards = ReplyKeyboardMarkup(keyboard=[
    [button_registr, button_exchange_rates],
    [button_tips, button_finances]
    ], resize_keyboard=True)

conn = sqlite3.connect('user_data.db')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY, 
    telegram_id INTEGER UNIQUE,
    name TEXT, 
    category1 TEXT,
    category2 TEXT,
    category3 TEXT, 
    expenses1 REAL,
    expenses2 REAL,
    expenses3 REAL
    )
''')
conn.commit()

class FinancesForm(StatesGroup):
    category1 = State()
    expenses1 = State()
    category2 = State()
    expenses2 = State()
    category3 = State()
    expenses3 = State()




@dp.message(Command('start'))
async def start(message: Message):
    await message.answer("Привет, я ваш личный финансовый помощник. Выберите одну из опций в меню", reply_markup=keyboards)

@dp.message(F.text == "Регистрация")
async def registration(message: Message):
    telegram_id = message.from_user.id
    name = message.from_user.full_name
    cur.execute('''SELECT * FROM users WHERE telegram_id = ?''', (telegram_id,))
    user = cur.fetchone()
    if user:
        await message.answer("Вы уже зарегистрированы")

    else:
        cur.execute('''INSERT INTO users (telegram_id, name) VALUES (?, ?)''', (telegram_id, name))
        conn.commit()
        await message.answer("Регистрация прошла успешно")


@dp.message(F.text == "Курсы валют")
async def exchange_rates(message: Message):
    url = 'https://v6.exchangerate-api.com/v6/d1ec190665fc1c2f6427efff/latest/USD'
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer("Произошла ошибка при получении курса валют")
            return
        usd_to_rub = data['conversion_rates']['RUB']
        eur_to_usd = data['conversion_rates']['EUR']

        eur_to_rub = eur_to_usd * usd_to_rub

        await message.answer(f"1 USD = {usd_to_rub:.2f} RUB\n1"
                             f"1 EUR = {eur_to_rub:.2f} RUB")

    except:
        await message.answer("Произошла ошибка при получении курса валют")

@dp.message(F.text == "Советы по экономии")
async def tips(message: Message):
    tips = [
        "Совет 1: Ведите бюджет и следите за своими расходами.",
        "Совет 2: Откладывайте часть доходов на сбережения.",
        "Совет 3: Покупайте товары по скидкам и распродажам."
    ]
    tip = random.choice(tips)
    await message.answer(tip)

@dp.message(F.text == "Финансы")
async def finances(message: Message, state: FSMContext):
    await state.set_state(FinancesForm.category1)
    await message.reply("Введите первую категорию расходов:")

@dp.message(FinancesForm.category1)
async def finances(message: Message, state: FSMContext):
   await state.update_data(category1=message.text)
   await state.set_state(FinancesForm.expenses1)
   await message.reply("Введите расходы для категории 1:")


@dp.message(FinancesForm.expenses1)
async def finances(message: Message, state: FSMContext):
    await state.update_data(expenses1=message.text)
    await state.set_state(FinancesForm.category2)
    await message.reply("Введите вторую категорию расходов:")


@dp.message(FinancesForm.category2)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category2=message.text)
    await state.set_state(FinancesForm.expenses2)
    await message.reply("Введите расходы для категории 2:")

@dp.message(FinancesForm.expenses2)
async def finances(message: Message, state: FSMContext):
    await state.update_data(expenses2=message.text)
    await state.set_state(FinancesForm.category3)
    await message.reply("Введите третью категорию расходов:")

@dp.message(FinancesForm.category3)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category3=message.text)
    await state.set_state(FinancesForm.expenses3)
    await message.reply("Введите расходы для категории 3:")

@dp.message(FinancesForm.expenses3)
async def finances(message: Message, state: FSMContext):
    data = await state.get_data()
    telegram_id = message.from_user.id
    cur.execute('''
    UPDATE users SET category1 = ?, expenses1 = ?, category2 = ?, expenses2 = ?, category3 = ?, expenses3 = ? WHERE telegram_id = ?''',
                (data['category1'], data['expenses1'], data['category2'], data['expenses2'], data['category3'], float(message.text), telegram_id))
    conn.commit()
    await state.clear()

    await message.answer("Категории и расходы сохранены")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())