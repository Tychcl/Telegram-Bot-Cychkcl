from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

def inkb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Картинки 🖼", callback_data='needpins')],
        [InlineKeyboardButton(text="Категории 📝", callback_data='categoryes')],
        [InlineKeyboardButton(text="Отмена ❌", callback_data='cancelPin')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def images():
    inline_kb_list = [
        [InlineKeyboardButton(text="Свои 🔮", callback_data='selfpins')],
        [InlineKeyboardButton(text="Все 🌌", callback_data='allpins')],
        [InlineKeyboardButton(text="⏪", callback_data='backPage'),
        InlineKeyboardButton(text="❌", callback_data='cancelPin')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def categoryes():
    inline_kb_list = [
        [InlineKeyboardButton(text="Изменить ♻", callback_data='changepin')],
        [InlineKeyboardButton(text="Добавить ➕", callback_data='addpin')],
        [InlineKeyboardButton(text="Удалить 🗑", callback_data='deletepin')],
        [InlineKeyboardButton(text="⏪", callback_data='backPage'),
        InlineKeyboardButton(text="❌", callback_data='cancelPin')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)