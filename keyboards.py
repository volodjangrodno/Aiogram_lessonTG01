from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# первый способ создания клавиатуры reply
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Тестовая кнопка 1")], # в этом ряду будет только одна кнопка
    [KeyboardButton(text="Тестовая кнопка 2"), KeyboardButton(text="Тестовая кнопка 3")] # в этом ряду будет две кнопки
], resize_keyboard=True)

# второй способ создания клавиатуры inline с внешними ссылками
inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Видео", url="https://youtu.be/dQw4w9WgXcQ"),
    InlineKeyboardButton(text="Аудио", url="https://pixabay.com/ru/sound-effects/elemental-magic-spell-impact-outgoing-228342/"),
    InlineKeyboardButton(text="Фото", url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqWe0SxHi3yrVJullGTT8aJp8sqTLdmJNQYQ&s")]
])

# ещё один способ создания клавиатуры inline с callback-запросами
inline_keyboard_test_2 = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Каталог", callback_data='catalog')],
   [InlineKeyboardButton(text="Новости", callback_data='news')],
   [InlineKeyboardButton(text="Профиль", callback_data='person')]
])

# третий способ создания клавиатуры builder
test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]

async def test_keyboard():
    keyboard = ReplyKeyboardBuilder()
    for key in test:
        keyboard.add(KeyboardButton(text=key))
    return keyboard.adjust(2).as_markup() # в одном ряду будет по две кнопки

async def test_keyboard2():
    keyboard = InlineKeyboardBuilder() # создаем инлайн клавиатуру
    for key in test:
        keyboard.add(InlineKeyboardButton(text=key, url="https://youtu.be/dQw4w9WgXcQ"))
    return keyboard.adjust(2).as_markup() # в одном ряду будет по две кнопки