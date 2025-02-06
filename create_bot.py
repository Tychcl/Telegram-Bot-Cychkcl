import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
#Импортируем функцию config из библиотеки python-decouple для загрузки переменных окружения из файла .env.
from apscheduler.schedulers.asyncio import AsyncIOScheduler
#Импортируем класс AsyncIOScheduler из библиотеки APScheduler для планирования задач (например, выполнение скриптов по времени).
all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_media')
#from db_handler.db_class import PostgresHandler

#pg_db = PostgresHandler(config('PG_LINK'))

scheduler = AsyncIOScheduler(timezone='Asia/Yekaterinburg') 
#Создаем объект AsyncIOScheduler для планирования и выполнения задач по времени. Устанавливаем часовой пояс на Europe/Moscow.
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]
creator = int(config('CREATOR'))
group = config('GROUP')
members = [int(admin_id) for admin_id in config('MEMBERS').split(',')]
#Создаем список ID администраторов бота. Загружаем строку с ID администраторов 
#из переменной окружения ADMINS, разделяем её по запятым и преобразуем каждый элемент в целое число.

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#Настраиваем базовое логирование с уровнем INFO, чтобы записывать важные сообщения. 
#Устанавливаем формат логов, включающий время, имя логгера и уровень сообщения.
logger = logging.getLogger(__name__)
#Создаем логгер с именем текущего модуля, чтобы записывать лог-сообщения.

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#Создаем объект Bot с токеном, загруженным из переменной окружения TOKEN. 
#По умолчанию прописал, чтоб бот корректно вопринимал HTML теги для форматирования текста (заслуживает отдельного обсуждения).
dp = Dispatcher(storage=MemoryStorage())
#это основной объект, отвечающий за обработку входящих сообщений и других обновлений, поступающих от Telegram. 
#Именно через диспетчер проходят все сообщения и команды, отправляемые пользователями бота.
#storage=MemoryStorage() указывает, что для хранения состояния конечных автоматов (FSM) используется память (RAM). 
#Это значит, что состояния пользователей будут храниться в оперативной памяти (тема большой отдельной статьи).
#FSM (Finite State Machine) используется для управления состояниями диалога с пользователем.
#Это позволяет боту "помнить" текущий шаг разговора и реагировать на действия пользователя в соответствии с текущим состоянием.