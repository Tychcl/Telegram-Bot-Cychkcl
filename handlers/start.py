from create_bot import bot, creator, group
from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, File, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery,FSInputFile,InlineKeyboardMarkup,InlineKeyboardButton
from keyboards.start_kb import main_kb
from aiogram.fsm.context import FSMContext
from pydub import AudioSegment
import random
import json
import time
import os

start_router = Router()

#@start_router.startup()
#async def startup():
#    set = await bot.get_sticker_set("stiki18tg189_by_fStikBot")
#    files = []
#    for x in set.stickers:
#        files.append(x.file_id)
#    print(files)

@start_router.message(Command("voice2txt"))
async def FindVoice(message: Message):
    try:
        msg = message.reply_to_message.voice
    except:
        await message.answer("Нет прикрепленного ГС в ответе\n(Ответь на нужное ГС командой \"/voice2txt\")")
        return
    if msg and msg.file_size < 5242880:
        path = f"handlers/Voices/voice{message.message_id}_{message.chat.id}.ogg"
        file = await bot.get_file(msg.file_id)
        await bot.download_file(file.file_path, destination=path)
        if os.path.exists(path):
            audio = AudioSegment.from_file(os.path.abspath(path))
            audio.export(path, format="mp3")
        else:
            print("no")
        

@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.delete()
    await state.clear()
    with open("handlers/stickers_start.json","r",encoding="utf-8") as f:
        data = json.load(f)
    await message.answer_sticker(sticker=random.choice(data),reply_markup=main_kb(message))
    print(message.from_user.id, message.chat.id)
    #await message.answer(text="test", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="test", callback_data=f'test{message.from_user.id}')]]))

#@start_router.callback_query(F.data.contains('test'))
#async def test_call(call:CallbackQuery):
    #await call.answer(text=call.data)