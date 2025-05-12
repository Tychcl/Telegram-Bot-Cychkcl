from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def inkb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Картинка 🖼", callback_data='image')],
        [InlineKeyboardButton(text="Текст/Ответ(WIP) 📓", callback_data='text')],
        [InlineKeyboardButton(text="Отмена ❌", callback_data='cancel')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list), "Что хочешь сделать?"

def format():
    inline_kb_list = [
        [InlineKeyboardButton(text="Квадрат 🔳", callback_data='square.1024.1024')],
        [InlineKeyboardButton(text="Пейзаж 🖼", callback_data='land.1024.512')],
        [InlineKeyboardButton(text="Портрет 🎴", callback_data='port.512.1024')],
        [InlineKeyboardButton(text="⏪", callback_data='back'), InlineKeyboardButton(text="❌", callback_data='cancel')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list), "Выбери формат"

def prompt():
    inline_kb_list = [
        [InlineKeyboardButton(text="⏪", callback_data='back'), InlineKeyboardButton(text="❌", callback_data='cancel')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list), "Напиши промпт"

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