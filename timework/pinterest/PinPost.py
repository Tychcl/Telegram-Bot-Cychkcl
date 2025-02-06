from create_bot import bot
from create_bot import group
from aiogram.types import InputMediaPhoto
from aiogram.utils.markdown import hlink
import os
import json
import requests
import numpy as np
from random import randint, shuffle
from urllib.parse import quote

count = 250

async def ClrQR():
    dir_name = "timework/pinterest/QRes"
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".json"):
            os.remove(os.path.join(dir_name, item))

async def get_pins(text: str, count: int, bookmark: str = None):
    url = "https://ru.pinterest.com/resource/BaseSearchResource/get/"
    data = {
        "options": {
            "query": text,
            "page_size": count,
            "scope": "pins",
            "redux_normalize_feed": True
        },
        "context": {}
    }
    
    if bookmark:
        data["options"]["bookmarks"] = [bookmark]  # добавляем bookmark для пагинации
    
    params = {
        "source_url": f"/search/pins/?q={text}",
        "data": json.dumps(data)
    }
    
    r = requests.get(url, params=params)
    return r.json()

async def fetch_all_pins(text: str, count: int):
    all_pins = []
    bookmark = None
    
    while True:
        response = await get_pins(text, count, bookmark)
        try:
            data = response["resource_response"]["data"]["results"]
        except:
            break
        
        if not data:
            break  # Если новых данных нет, останавливаемся
        
        pins = list(map(lambda z: z["images"]["orig"]["url"], data))
        all_pins.extend(pins)
        
        # Проверяем, есть ли bookmark для продолжения запроса
        bookmark = response["resource"]["options"].get("bookmarks")
        if not bookmark:
            break  # Если bookmark нет, прекращаем цикл

    return all_pins

async def SelfPins(id: int, chat: int):
    with open("timework/pinterest/CatPins.json","r",encoding="utf-8") as f:
        data = json.load(f)
    files = os.listdir("timework/pinterest/QRes")
    PinsUsed = []
    PinsToSend = []
    end = ""
    mem = await bot.get_chat_member(chat_id=chat,user_id=id)
    for index, category in enumerate(data[str(id)]):
        cat = category["category"]
        file = quote(cat)+".json"
        if file[-50:len(file)] not in files:
            pins = await fetch_all_pins(cat, count)
            print(f"Всего картинок собрано: {len(pins)} по запросу {cat}")
            with open(f"timework/pinterest/QRes/{file[-50:len(file)]}", "w", encoding="utf-8") as f:
                json.dump(pins, f, indent=2, ensure_ascii=False)
        else:
            with open(f"timework/pinterest/QRes/{file[-50:len(file)]}","r",encoding="utf-8") as f:
                pins = json.load(f)
        NotUsed = np.setdiff1d(pins, category["used"])
        if len(NotUsed) < 3:
            end+=(f"Пины по запросу <b>{category}</b> от @{mem.user.username} отсутствуют 😣\n")
        else:
            i = 0
            while i != 3:
                rnd = randint(0,len(NotUsed)-1)
                if(NotUsed[rnd] not in PinsUsed):
                    PinsUsed.append(NotUsed[rnd])
                    PinsToSend.append([NotUsed[rnd],cat])
                    category["used"].append(NotUsed[rnd])
                    i+=1
    with open("timework/pinterest/CatPins.json","w",encoding="utf-8") as f:
        json.dump(data,f,indent=2,ensure_ascii=False)
    media = [InputMediaPhoto(media=send[0], caption=hlink(send[1], str(send[0]))) for send in PinsToSend]
    await bot.send_media_group(chat_id=chat,media=media)
    if(end != ""):
        await bot.send_message(chat_id=chat,text=end)

async def AllPins():
    with open("timework/pinterest/CatPins.json","r",encoding="utf-8") as f:
        data = json.load(f)
    files = os.listdir("timework/pinterest/QRes")
    PinsToSend = []
    end = ""
    for key in data.keys():
        for category in data[key]:
            cat = category["category"]
            file = quote(cat)+".json"
            if file[-50:len(file)] not in files:
                pins = await fetch_all_pins(cat, count)
                print(f"Всего картинок собрано: {len(pins)} по запросу {cat}")
                with open(f"timework/pinterest/QRes/{file[-50:len(file)]}", "w", encoding="utf-8") as f:
                    json.dump(pins, f, indent=2, ensure_ascii=False)
            else:
                with open(f"timework/pinterest/QRes/{file[-50:len(file)]}","r",encoding="utf-8") as f:
                    pins = json.load(f)
            NotUsed = np.setdiff1d(pins, category["used"])
            if len(NotUsed) < 1:
                end+=(f"Пины по запросу <b>{category}</b> от @{int(key).user.username} отсутствуют 😣\n")
            else:
                rnd = randint(0,len(NotUsed)-1)
                PinsToSend.append([NotUsed[rnd],cat])
                category["used"].append(NotUsed[rnd])
    with open("timework/pinterest/CatPins.json","w",encoding="utf-8") as f:
        json.dump(data,f,indent=2,ensure_ascii=False)
    media = [InputMediaPhoto(media=send[0], caption=hlink(send[1], send[0])) for send in PinsToSend]
    await bot.send_media_group(chat_id=group,media=media)
    if(end != ""):
        await bot.send_message(chat_id=group,text=end)