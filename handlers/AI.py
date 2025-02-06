from create_bot import bot
from aiogram import Router, F
from aiogram.types import Message,CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.AI_inln import inkb, format,keyboard
from keyboards.start_kb import main_kb
from g4f.client import Client
import datetime
import json
import time
import requests
import base64
from urllib.parse import quote
import os

AI_router = Router()

@AI_router.message(F.text == "Нейроночка 🧠")
async def kb(message: Message, state: FSMContext):
    await state.clear()
    await message.delete()
    await message.answer("Что хочешь сделать?",reply_markup=inkb())

#ГЕНЕРАЦИЯ КАРТИНОК
class Text2ImageAPI:
    
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, width, height, images=1 ):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=20, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

async def ImageGen(prompt, width, height):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '04B2A6EE169885AB26DC49E5099C2A46', '6C4C179243BFBF36D20214DCD20A2869')
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id, width, height)
    images = api.check_generation(uuid)
    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)
    date = str(datetime.datetime.now()).split(" ")
    date = date[0].replace("-","_") + "_" + date[1].replace(":","_").replace(".","_")
    prompt = quote(prompt)
    name = f"{prompt.split('.')[0]}_{date}.jpg"
    try:
        with open(f"handlers/AIImages/{name[-50:len(name)]}", "wb") as file:
            file.write(image_data)
    except:
        with open(f"handlers/AIImages/{name[-50:len(name)]}", "w+") as file:
            file.write(image_data)
    return f"handlers/AIImages/{name[-50:len(name)]}"

class Image(StatesGroup):
    form = State()
    prompt = State()
    chatid = State()
    botmsgid = State()

@AI_router.message(F.text, Image.prompt)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(prompt=message.text)
    data = await state.get_data()
    await state.set_state(None)
    await bot.edit_message_text(chat_id=message.chat.id,message_id=data['botmsgid'], text="Идет генерация")
    path = await ImageGen(data['prompt'], data['form'][0], data['form'][1])
    photo_file = FSInputFile(path=path)
    await message.answer_photo(photo=photo_file, reply_markup=keyboard(), caption=data['prompt'])
    await bot.delete_message(chat_id=message.chat.id, message_id=data['botmsgid'])
    os.remove(path)

@AI_router.message(F.text == "Еще раз ♻")
async def AIagainImage(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    o = await message.answer(text="Идет генерация", reply_markup=main_kb(message))
    path = await ImageGen(data['prompt'], data['form'][0], data['form'][1])
    photo_file = FSInputFile(path=path)
    await message.answer_photo(photo=photo_file, reply_markup=keyboard(), caption=data['prompt'])
    await o.delete()
    os.remove(path)

@AI_router.callback_query(F.data == 'image')
async def AIimage(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=call.message.chat.id ,message_id=call.message.message_id, text="Выбери формат", reply_markup=format(''))
    await state.update_data(chatid=call.message.chat.id)
    await state.update_data(botmsgid=call.message.message_id)

@AI_router.message(F.text == "Сменить промпт ✏")
async def newprompt(message: Message, state: FSMContext):
    await message.delete()
    o = await bot.send_message(chat_id=message.chat.id ,text="Напиши промпт для картинки", 
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отмена ❌", callback_data='cancel')]]))
    await state.update_data(botmsgid=o.message_id)
    await state.update_data(chatid=o.chat.id)
    await state.set_state(Image.prompt)

#ФОРМАТЫ
@AI_router.message(F.text == "Сменить формат 🎨")
async def newformat(message: Message):
    await message.delete()
    await message.answer(text="Выбери формат", reply_markup=format('again'))

@AI_router.callback_query(F.data.contains('square'))
async def squareimage(call: CallbackQuery, state: FSMContext):
    await state.update_data(form=[1024,1024])
    if call.data.__contains__('again'):
        await AIagainImage(call.message, state)
        return
    await bot.edit_message_text(chat_id=call.message.chat.id ,message_id=call.message.message_id, text="Напиши промпт для картинки", 
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отмена ❌", callback_data='cancel')]]))
    await state.set_state(Image.prompt)

@AI_router.callback_query(F.data.contains('landscape'))
async def landscapeimage(call: CallbackQuery, state: FSMContext):
    await state.update_data(form=[1024,576])
    if call.data.__contains__('again'):
        await AIagainImage(call.message, state)
        return
    await bot.edit_message_text(chat_id=call.message.chat.id ,message_id=call.message.message_id, text="Напиши промпт для картинки", 
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отмена ❌", callback_data='cancel')]]))
    await state.set_state(Image.prompt)

@AI_router.callback_query(F.data.contains('portrait'))
async def portraitimage(call: CallbackQuery, state: FSMContext):
    await state.update_data(form=[576,1024])
    if call.data.__contains__('again'):
        await AIagainImage(call.message, state)
        return
    await bot.edit_message_text(chat_id=call.message.chat.id ,message_id=call.message.message_id, text="Напиши промпт для картинки", 
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отмена ❌", callback_data='cancel')]]))
    await state.set_state(Image.prompt)

#ГЕНЕРАЦИЯ ОТВЕТОВ

#class AIText(StatesGroup()):
    #prompt = State()
    #response = State()



#ОТМЕНА
@AI_router.callback_query(F.data.contains('cancel'))  # Сработает при команде /cancel
async def cancel_handler(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer(text="Оке :D", reply_markup=main_kb(call.message))
    if len(call.data) > len('cancel'):
        await call.message.edit_reply_markup(reply_markup=None)
        return
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