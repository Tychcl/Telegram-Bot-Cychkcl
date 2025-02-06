import asyncio
from create_bot import bot, dp, scheduler, group, creator, admins, members
from handlers.start import start_router
from handlers.PinUpd import Pinterest_router
from handlers.AI import AI_router
from timework.pinterest.PinPost import ClrQR, AllPins
from timework.Aviat.pairs import SendPairsMsg
from timework.Weather.Weather import SendWeather

from typing import Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.utils.markdown import hlink

class NAHUI(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()
        #self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, any]], Awaitable[any]],  # Используем Awaitable
        event: Message,
        data: Dict[str, any]
    ) -> Awaitable[any]:  # Указываем, что метод возвращает Awaitable
        #self.counter += 1
        #data['counter'] = self.counter
        #return await handler(event, data)  # Ожидаем выполнения обработчика
        memid = event.from_user.id
        mem = await bot.get_chat_member(chat_id=group,user_id=memid)
        if(((mem.status != "left" and mem.status != "kicked")) or memid == creator or memid in admins or memid in members):
            return await handler(event, data)

async def main():
#Определяем основную асинхронную функцию main, которая будет запускаться при старте бота
    scheduler.add_job(AllPins, 'cron', hour='10,14,18,22')
    scheduler.add_job(SendWeather, 'cron', hour='7')
    #scheduler.add_job(SendPairsMsg, 'interval', seconds=60*10)

    #scheduler.add_job(ClrQR, 'interval', seconds=60*60*24*7)
    
    scheduler.start()
#Добавляем задачу в планировщик scheduler. Задача send_time_msg будет выполняться каждые 10 секунд. Запускаем
    dp.message.middleware(NAHUI())
    dp.include_router(start_router)
    dp.include_router(Pinterest_router)
    dp.include_router(AI_router)
#Добавляем роутер start_router в диспетчер dp. 
#Это позволяет диспетчеру знать о всех обработчиках команд, которые определены в start_router.
    await bot.delete_webhook(drop_pending_updates=True)
#Несмотря на то, что мы работаем через метод лонг поллинга, данная строка так же будет корректной. 
#В тройке это аналог записи: skip_updates=True из более старых версий aiogram
    await dp.start_polling(bot)
#Запускаем бота в режиме опроса (polling). Бот начинает непрерывно запрашивать обновления с сервера Telegram и обрабатывать их.

if __name__ == "__main__":
    asyncio.run(main())