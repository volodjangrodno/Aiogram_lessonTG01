import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN

import random

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('photo'))
async def send_photo(message: Message):
    list = ['https://kartinki.pics/pics/uploads/posts/2022-09/1662615787_1-kartinkin-net-p-milie-kotiki-v-shapochkakh-instagram-1.jpg', 'https://st2.depositphotos.com/1886175/8316/i/450/depositphotos_83169300-stock-photo-gray-striped-cat-playful-cute.jpg', 'https://static3.depositphotos.com/1005412/218/i/450/depositphotos_2186038-stock-photo-kitten-lays-isolated.jpg', 'https://static5.depositphotos.com/1038294/457/i/450/depositphotos_4577097-stock-photo-kitten-with-his-paw-raised.jpg', 'https://static3.depositphotos.com/1000627/109/i/450/depositphotos_1095588-stock-photo-green-eyed-cat.jpg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка!')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Очень плохое фото', 'Плохое фото', 'Нормальное фото', 'Хорошее фото', 'Отличное фото']
    rand_answer = random.choice(list)
    await message.answer(rand_answer)

@dp.message(F.text == "Привет")
async def answer(message: Message):
    await message.answer(f"Слушаю и повинуюсь, {message.from_user.full_name}!")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Я твой бот-помощник.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())