import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
import requests
from deep_translator import GoogleTranslator

from config import TOKEN, THE_CAT_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_cat_breads():
    url = 'https://api.thecatapi.com/v1/breeds'
    headers = {'x-api-key': THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def get_cat_image_by_bread(bread_id):
    url = f'https://api.thecatapi.com/v1/images/search?breed_ids={bread_id}'
    headers = {'x-api-key': THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url']

def get_bread_info(bread_name):
    breads = get_cat_breads()
    for bread in breads:
        if bread['name'].lower() == bread_name.lower():
            return bread
    return None

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, напиши мне название породы кошки , и я пришлю фотку и информацию о ней")

@dp.message()
async def send_cat_info(message: Message):
    bread_name = message.text
    bread_info = get_bread_info(bread_name)
    if bread_info:
        cat_image_url = get_cat_image_by_bread(bread_info['id'])
        # Используем deep_translator для перевода
        translator = GoogleTranslator(source='en', target='ru')
        translated_name = translator.translate(bread_info["name"])
        translated_description = translator.translate(bread_info["description"])

        info = (f'Порода: {translated_name}\n'
                f'Описание: {translated_description}\n'
                f'Продолжительность жизни: {bread_info["life_span"]} лет\n')

        await message.answer_photo(photo=cat_image_url, caption=info)

    else:
        await message.answer("Кошка такой породы не найдена")



async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())