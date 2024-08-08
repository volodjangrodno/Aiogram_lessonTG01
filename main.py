import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from gtts import gTTS
import os

from config import TOKEN

import random

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('photo')) # Когда мы отправляем любую команду боту в Telegram,
# по умолчанию используется слэш (/) перед командой.
# Но мы можем задать и свои префиксы. Например &. И тогда команда будет вызываться &photo.
async def send_photo(message: Message):
    list = ['https://kartinki.pics/pics/uploads/posts/2022-09/1662615787_1-kartinkin-net-p-milie-kotiki-v-shapochkakh-instagram-1.jpg',
            'https://st2.depositphotos.com/1886175/8316/i/450/depositphotos_83169300-stock-photo-gray-striped-cat-playful-cute.jpg',
            'https://static3.depositphotos.com/1005412/218/i/450/depositphotos_2186038-stock-photo-kitten-lays-isolated.jpg',
            'https://static5.depositphotos.com/1038294/457/i/450/depositphotos_4577097-stock-photo-kitten-with-his-paw-raised.jpg',
            'https://static3.depositphotos.com/1000627/109/i/450/depositphotos_1095588-stock-photo-green-eyed-cat.jpg'
            ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка!')
    # Здесь бот высылает нам рандомную картинку из списка list с указанным текстом

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Очень плохое фото', 'Плохое фото', 'Нормальное фото', 'Хорошее фото', 'Отличное фото']
    rand_answer = random.choice(list)
    await message.answer(rand_answer) # рандомный ответ бота на фото из списка ответов list
    await bot.download(message.photo[-1].file_id, f'tmp/{message.photo[-1].file_id}.jpg')
    # здесь бот скачивает высланное собеседником фото в указанную папку tmp и присваивает ему имя с индексом [-1].

@dp.message(F.text == "Привет") # ответ бота на сообщение от нас "Привет"
async def answer(message: Message):
    await message.answer(f"Слушаю и повинуюсь, {message.from_user.full_name}!")

@dp.message(Command('video')) # Здесь бот высылает видео по команде /video
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video') # Здесь бот подтверждает действие "upload_video" в чате
    video = FSInputFile('video.mp4')
    await bot.send_video(message.chat.id, video)

@dp.message(Command('audio')) # Здесь бот высылает аудио по команде /audio
async def audio(message: Message):
    audio = FSInputFile('audio.mp3')
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('training')) # Здесь бот высылает рандомную тренировку по команде /training и озвучивает её
async def training(message: Message):
    training_list = [
        "Тренировка 1: \n 1. Приседания с весом тела - 3 подхода по 15 повторений. \n 2. Отжимания - 3 подхода по 10 повторений. \n3. Выпады вперед - 3 подхода по 12 повторений на каждую ногу. \n 4. Планка (статическое удержание) - 3 подхода по 1 минуте. \n 5. Супермен (подъемы рук и ног лежа на животе) - 3 подхода по 15 повторений.",
        "Тренировка 2: \n 1. Бёрпи - 3 подхода по 10 повторений. \n 2. Прыжки через скакалку - 3 подхода по 1 минуте. \n 3. Альпинисты (Mountain Climbers) - 3 подхода по 30 секунд. \n 4. Высокие колени (High Knees) - 3 подхода по 1 минуте. \n 5. Бег на месте с ускорениями (интервалы 30 секунд обычный бег, 30 секунд ускорение) - 3 подхода.",
        "Тренировка 3: \n 1. Йога поза Собака мордой вниз - удержание 1 минута. \n 2. Поза Воин 1 - удержание по 1 минуте на каждую ногу. \n 3. Поза Планка - удержание 1 минута. \n 4. Подъемы на носки стоя (для икроножных мышц) - 3 подхода по 15 повторений. \n 5. Баланс на одной ноге с касанием пола - 3 подхода по 10 повторений на каждую ногу."
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr} \n")

    tts = gTTS(text=rand_tr, lang='ru') # преобразование текста тренировки в аудио
    tts.save('training.mp3') # сохранение аудио
    audio = FSInputFile('training.mp3')
    await bot.send_audio(message.chat.id, audio) # отправка аудио в чат
    os.remove('training.mp3') # удаление аудио

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help \n /photo")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Я твой бот-помощник.")

@dp.message() # ответ бота на все остальные сообщения, кроме текста "стоп" с маленькими буквами
async def all_answer(message: Message):
    if message.text.lower() == "стоп":
        await message.answer(f"Стою - не двигаюсь, {message.from_user.full_name}!")
    else:
        await message.answer(f"Принято, {message.from_user.full_name}! Уже метнулся исполнять команду.")

# @dp.message() # ответ бота тем же сообщением (эхо-бот)
# async def echo(message: Message):
#     await message.send_copy(chat_id=message.chat.id)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())