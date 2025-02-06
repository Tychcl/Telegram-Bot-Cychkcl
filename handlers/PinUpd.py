from create_bot import bot
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery, InputFile, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from timework.pinterest.PinPost import SelfPins, AllPins
from keyboards.PIN_inln import inkb, images, categoryes
from create_bot import group, creator, admins
import json

Pinterest_router = Router()

lastPage = State()

class Pinterest(StatesGroup):
    msgid = State()
    cat = State()

class Change(StatesGroup):
    msgid = State()
    i = State()
    cat = State()

@Pinterest_router.message(F.text == 'Пинтерест 🐱‍🏍')
async def MainPinterestHandler(message: Message, state: FSMContext):
    await state.clear()
    await message.delete()
    await message.answer("Что необходимо?",reply_markup=inkb())

#КАРТИНКИ
@Pinterest_router.callback_query(F.data == 'needpins') 
async def NeedPins(call: CallbackQuery, state: FSMContext):
    await state.update_data(lastPage="main")
    await call.message.edit_text(text="Какие картинки хочешь?", reply_markup=images())

@Pinterest_router.callback_query(F.data == 'selfpins') 
async def MyPins(call: CallbackQuery):
    await call.message.edit_text(text="Отправляю 💀", reply_markup=None)
    await SelfPins(call.from_user.id, call.message.chat.id)
    await call.message.delete()

@Pinterest_router.callback_query(F.data == 'allpins') 
async def GlobalPins(call: CallbackQuery):
    await call.message.edit_text(text="Отправляю 💀", reply_markup=None)
    await AllPins(call.message.chat.id)
    await call.message.delete()

#КАТЕГОРИИ
@Pinterest_router.callback_query(F.data == 'categoryes') 
async def CategoryesHandler(call: CallbackQuery, state: FSMContext):
    await state.update_data(lastPage="main")
    await call.message.edit_text(text="Что хочешь сделать?", reply_markup=categoryes())

#ИЗМЕНЕНИЕ
@Pinterest_router.callback_query(F.data == 'changepin') 
async def ChangePin(call: CallbackQuery, state: FSMContext):
    await state.update_data(lastPage="categoryes")
    userid = call.from_user.id
    with open("timework/pinterest/CatPins.json","r",encoding="utf-8") as f:
        data = json.load(f)
    cat = ""
    num = ["1️⃣","2️⃣","3️⃣"]
    list = []
    if str(userid) in data.keys() and len(data[str(userid)]) > 0:
        for i,x in enumerate(data[str(call.from_user.id)]):
            cat += f"{i+1}) {x['category'].replace("<", "&lt;").replace(">", "&gt;")}\n"
            list.append(InlineKeyboardButton(text=num[i], callback_data=f"ChangePinByNum{i}"))
        await call.message.edit_text(text=f"Выбери что изменить:\n{cat}",
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[list,[InlineKeyboardButton(text="⏪", callback_data='backPage'), InlineKeyboardButton(text="❌", callback_data='cancelPin')]]))
    else:
        call.message.edit_text(text="Нечего изменять☹\nСделать?",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Добавить ➕", callback_data='addpin')],[InlineKeyboardButton(text="Отмена ❌", callback_data='cancelPin')]]))
    
@Pinterest_router.callback_query(F.data.contains("ChangePinByNum")) 
async def DelPinByNum(call: CallbackQuery, state: FSMContext):
    await state.update_data(i=int(call.data.replace("ChangePinByNum","")))
    await state.update_data(msgid=call.message.message_id)
    await call.message.edit_text(text="Напиши на что заменить✏", reply_markup=None)
    await state.set_state(Change.cat)

@Pinterest_router.message(F.text, Change.cat)
async def ChangeCat(message:Message,state:FSMContext):
    await state.update_data(cat=message.text)
    with open("timework/pinterest/CatPins.json","r",encoding="utf-8") as f:
        data = json.load(f)
    statedata = await state.get_data()
    data[str(message.from_user.id)][statedata["i"]] = {"category":statedata["cat"],"used":[]}
    with open("timework/pinterest/CatPins.json","w",encoding="utf-8") as f:
        json.dump(data,f,indent=2,ensure_ascii=False)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=statedata["msgid"], text="Изменено✅")
    await message.delete()
    await state.clear()
    await state.set_state(None)

#ДОБАВЛЕНИЕ
@Pinterest_router.callback_query(F.data == 'addpin') 
async def AddPin(call: CallbackQuery, state: FSMContext):
    await state.update_data(lastPage="categoryes")
    userid = call.from_user.id
    with open("timework/pinterest/CatPins.json","r",encoding="utf-8") as f:
        data = json.load(f)
    if str(userid) not in data.keys() or len(data[str(userid)]) < 3:
        await call.message.edit_text(text="Напиши категорию✏",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⏪", callback_data='backPage'), InlineKeyboardButton(text="❌", callback_data='cancelPin')]]))
        await state.update_data(msgid=call.message.message_id)
        await state.set_state(Pinterest.cat)
    elif len(data[str(userid)]) >= 3:
        await call.message.edit_text(text="Больше трех незя :3",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⏪", callback_data='backPage'), InlineKeyboardButton(text="❌", callback_data='cancelPin')]]))
        
@Pinterest_router.message(F.text, Pinterest.cat)
async def AddCategory(message:Message,state:FSMContext):
    await state.update_data(cat=message.text)
    statedata = await state.get_data()
    with open("timework/pinterest/CatPins.json","r",encoding="utf-8") as f:
        data = json.load(f)
    if str(message.from_user.id) not in data.keys():
        new = {str(message.from_user.id):[{"category":statedata["cat"], "used":[]}]}
        data = data | new
    else:
        new = {"category":statedata["cat"], "used":[]}
        data[str(message.from_user.id)].append(new)
    with open("timework/pinterest/CatPins.json","w",encoding="utf-8") as f:
        json.dump(data,f,indent=2,ensure_ascii=False)
        await bot.delete_message(chat_id=message.chat.id, message_id=statedata["msgid"])
        await message.answer("Категория добавилась➕")
        await message.delete()
        await state.clear()
        await state.set_state(None)

#УДАЛЕНИЕ
@Pinterest_router.callback_query(F.data == 'deletepin') 
async def DeletePin(call: CallbackQuery,state: FSMContext):
    await state.update_data(lastPage="categoryes")
    with open("timework/pinterest/CatPins.json","r",encoding="utf-8") as f:
        data = json.load(f)
    cat = ""
    num = ["1️⃣","2️⃣","3️⃣"]
    list = []
    for i,x in enumerate(data[str(call.from_user.id)]):
        cat += f"{i+1}) {x['category'].replace("<", "&lt;").replace(">", "&gt;")}\n"
        list.append(InlineKeyboardButton(text=num[i], callback_data=f"DelPinByNum{i}"))
    await call.message.edit_text(text=f"Выбери что удалить:\n{cat}",
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[list,[InlineKeyboardButton(text="Все🌌", callback_data=f"DelPinByNumAll")],[InlineKeyboardButton(text="⏪", callback_data='backPage'), InlineKeyboardButton(text="❌", callback_data='cancelPin')]]))

@Pinterest_router.callback_query(F.data.contains("DelPinByNum")) 
async def DelPinByNum(call: CallbackQuery):
    with open("timework/pinterest/CatPins.json","r",encoding="utf-8") as f:
        data = json.load(f)
    i = call.data.replace("DelPinByNum","")
    if i == "All":
        data[str(call.from_user.id)] = []
    else:
        data[str(call.from_user.id)].pop(int(i))
    with open("timework/pinterest/CatPins.json","w",encoding="utf-8") as f:
        json.dump(data,f,indent=2,ensure_ascii=False)
    await call.message.edit_text(text="Гатова :3", reply_markup=None)

#ОТМЕНА
@Pinterest_router.callback_query(F.data == 'backPage')  
async def back_handler(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    data = await state.get_data()
    print(data)
    if data["lastPage"] == "main":
        await call.message.edit_text("Что необходимо?",reply_markup=inkb())
    if data["lastPage"] == "categoryes":
        await state.update_data(lastPage="main")
        await call.message.edit_text(text="Что хочешь сделать?", reply_markup=categoryes())
    if current_state is None:  # Если его нет, то ничего не возвращаем
        return
    await state.set_state(None)

@Pinterest_router.callback_query(F.data == 'cancelPin')  
async def cancel_handler(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()  # Получаем текущий state
    await bot.delete_message(chat_id=call.message.chat.id ,message_id=call.message.message_id)
    if current_state is None:  # Если его нет, то ничего не возвращаем
        return
    await state.clear()
    await state.set_state(None)