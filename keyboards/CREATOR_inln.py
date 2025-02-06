from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def inkb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Небо посты", callback_data='pinsfortgk')],
        [InlineKeyboardButton(text="Отмена ❌", callback_data='cancel')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)