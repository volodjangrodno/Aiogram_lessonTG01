import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
import requests
from deep_translator import GoogleTranslator
from datetime import datetime, timedelta

from config import TOKEN, NASA_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365) # задаём start_date 365 дней назад
    random_data = start_date + (end_date - start_date) * random.random()
    data_str = random_data.strftime('%Y-%m-%d')

    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={data_str}'
    response = requests.get(url)

    return response.json()

@dp.message(Command('random_apod'))
async def random_apod(message: Message):
    apod = get_random_apod()
    photo_url = apod['url']
    title = apod['title']


    await message.answer_photo(photo=photo_url, caption=f'{title}')


async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())