from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins, creator

def main_kb(mes):
    kb_list = [
        [KeyboardButton(text="Нейроночка 🧠"), KeyboardButton(text="Пинтерест 🐱‍🏍")]#,
        #[KeyboardButton(text="Авиационный 🏢")]
    ]
    if mes.from_user.id in admins and mes.chat.type == "private" and mes.from_user.id != creator:
        kb_list.append([KeyboardButton(text="⚙️ Админ")])
    if mes.from_user.id == creator and mes.chat.type == "private":
        kb_list.append([KeyboardButton(text="💋 Создатель")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard