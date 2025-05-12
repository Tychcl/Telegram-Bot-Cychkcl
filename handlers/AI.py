from create_bot import bot
from aiogram import Router, F
from aiogram.types import Message,CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.AI_inln import inkb, format, keyboard, prompt
from multiprocessing import Process, Queue
from keyboards.start_kb import main_kb
import datetime
import json
import time
import requests
import base64
from urllib.parse import quote
import os
from g4f import Client

AI_router = Router()

def Use_AI(func: function, *args):
    result_queue = Queue()
    process = Process(target=func, args=args)
    process.start()
    process.join()
    return result_queue.get()

@AI_router.message(F.text == "Нейроночка 🧠")
async def AI_Menu(message: Message, state: FSMContext):
    await state.clear()
    await message.delete()
    reply, text = inkb()
    await message.answer(text=text,reply_markup=reply)

#ГЕНЕРАЦИЯ КАРТИНОК
class Image(StatesGroup):
    Prompt = State()
    Width = State()
    Height = State()
    ChatId = State()
    StartMessageId = State()
    LastInline = State()

def Get_Image(Prompt: str, Width: int, Height: int, result_queue):
    client = Client()
    response = client.images.generate(
    model="dall-e-3",
    prompt=Prompt,
    width=Width,
    height=Height,
    response_format="url" #Получаем ссылку на картинку вместо ее скачивания
    )
    result_queue.put(response.data[0].url)

@AI_router.callback_query(F.data == 'image')
async def Start_Image(call: CallbackQuery, state: FSMContext):
    msg = call.message
    await state.update_data(ChatId = msg.chat.id)
    await state.update_data(StartMessageId = msg.message_id)
    await state.update_data(LastInline = inkb())
    reply, text = format()
    await msg.edit_text(text=text, reply_markup=reply)

@AI_router.callback_query(F.data.contains('square.') or F.data.contains('land.') or F.data.contains('port.'))
async def Sqare_Format(call: CallbackQuery, state: FSMContext):
    wxh = call.data.split('.')
    await state.update_data(Width = int(wxh[1]))
    await state.update_data(Height = int(wxh[2]))
    await state.update_data(LastInline = format())
    reply, text = prompt()
    await call.message.edit_text(text=text, reply_markup=reply)
    await state.set_state(Image.Prompt)

@AI_router.message(F.text, Image.Prompt)
async def AI_Image_Generation(message: Message, state: FSMContext):
    await state.update_data(Prompt = message.text)
    data = await state.get_data()
    result_queue = Queue()
    process = Process(target=Get_Image, args=(data['Prompt'], data['Width'], data['Height'], result_queue))
    process.start()
    process.join()
    url = result_queue.get()
#ГЕНЕРАЦИЯ ОТВЕТОВ

class AIText(StatesGroup):
    context = State()
    prompt = State()

@AI_router.callback_query(F.data == 'back')  # Сработает при команде /cancel
async def back_handler(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    reply, text = data['LastInline']
    await call.message.edit_text(text=text, reply_markup=reply)

#ОТМЕНА
@AI_router.callback_query(F.data.contains('cancel'))  # Сработает при команде /cancel
async def cancel_handler(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer(text="Оке :D", reply_markup=main_kb(call.message))
    current_state = await state.get_state()  # Получаем текущий state
    await bot.delete_message(chat_id=call.message.chat.id ,message_id=call.message.message_id)
    if current_state is None:  # Если его нет, то ничего не возвращаем
        return
    await state.clear()
    await state.set_state(None)

@AI_router.message(F.text == "Отмена ❌")
async def cancel_kb(message: Message):
    await message.delete()
    await message.answer(text="Оке :D", reply_markup=main_kb(message)) #edit_reply_markup(reply_markup=main_kb(message))