from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def inkb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Картинка 🖼", callback_data='image')],
        [InlineKeyboardButton(text="Текст/Ответ(WIP) 📓", callback_data='text')],
        [InlineKeyboardButton(text="Отмена ❌", callback_data='cancel')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def format(x):
    inline_kb_list = [
        [InlineKeyboardButton(text="Квадрат 🔳", callback_data=f'square{x}')],
        [InlineKeyboardButton(text="Пейзаж 🖼", callback_data=f'landscape{x}')],
        [InlineKeyboardButton(text="Портрет 🎴", callback_data=f'portrait{x}')],
        [InlineKeyboardButton(text="Отмена ❌", callback_data=f'cancel{x}')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def keyboard():
    kb_list = [
        [KeyboardButton(text="Сменить промпт ✏")], 
        [KeyboardButton(text="Сменить формат 🎨")],
        [KeyboardButton(text="Еще раз ♻"), KeyboardButton(text="Отмена ❌")]
        #[KeyboardButton(text="Авиационный 🏢")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Что дальше?"
    )
    return keyboard