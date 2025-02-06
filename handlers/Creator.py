from create_bot import bot, creator, group
from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery,FSInputFile,InlineKeyboardMarkup,InlineKeyboardButton
from keyboards.CREATOR_inln import inkb
from keyboards.PIN_inln import images
from aiogram.fsm.context import FSMContext

Creator_router = Router()

@Creator_router.message(F.text == '💋 Создатель')
async def MainCreatorHandler(message: Message, state: FSMContext):
    id = message.from_user.id

    if id == creator:
        await message.delete()
        await message.answer("Что необходимо?",reply_markup=inkb())
    else:
        await message.answer("Тебе нельзя <3", reply_markup=None)

@Creator_router.callback_query(F.data == 'needpins') 
async def NeedPins(call: CallbackQuery):
    await call.message.edit_text(text="Какие картинки хочешь?", reply_markup=images())