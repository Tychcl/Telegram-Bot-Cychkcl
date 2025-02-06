from create_bot import bot, group
from aiogram.types import FSInputFile
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import time

sticks = ['CAACAgIAAxUAAWeUkN7S1FSoRsLI4_0DhAIKNBBHAAIRaAACGFKRSEtvo53S8mo5NgQ', 'CAACAgIAAxUAAWeUkN5GuWUIEAqP5PbD-Bl3jk-UAAILaQACRvqYSNK5U2gVyKL7NgQ', 'CAACAgIAAxUAAWeUkN7X_O57iIFq8-UcW7NOtIWwAALUZwACm-SZSIdbaAc0G6LyNgQ', 'CAACAgIAAxUAAWeUkN4tiVbXlWPix8XvdpnqeK1uAAK-bwAC1G-ZSHqfNu7YmVQyNgQ', 'CAACAgIAAxUAAWeUkN4NwNoP5588fGQo82nSC2CmAAJObgACeYWQSG2XvcNkCLS4NgQ', 'CAACAgIAAxUAAWeUkN6vb8yZdqLjdG1zD4Px_07lAAIVcQACgj2YSB9LIbMEd96XNgQ', 'CAACAgIAAxUAAWeUkN6g9IDuQrPHkkLQd4IjJHjCAAKgYwACBMuYSPVWb_NG7WsfNgQ']

async def SendWeather():
    path = "timework/Weather/"
    options = Options()
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    driver = webdriver.Edge(options=options)
    
    driver.get("https://yandex.ru/pogoda/ru-RU/perm/details")
    time.sleep(5)
    weather = driver.find_element(By.CLASS_NAME, "sc-b9164f35-1.ljXkQi")
    weather.screenshot(path+"WPermToday.png")

    driver.get("https://yandex.ru/pogoda/ru-RU/kazan/details")
    time.sleep(5)
    weather = driver.find_element(By.CLASS_NAME, "sc-b9164f35-1.ljXkQi")
    weather.screenshot(path+"WKazanToday.png")

    driver.quit()
    await bot.send_sticker(sticker=sticks[datetime.today().weekday()], chat_id=group)
    await bot.send_photo(photo=FSInputFile(path=path+"WPermToday.png"), caption="Пермь погода🌆", chat_id=group)
    await bot.send_photo(photo=FSInputFile(path=path+"WKazanToday.png"), caption="Казань погода🌆", chat_id=group)