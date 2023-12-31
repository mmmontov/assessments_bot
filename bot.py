import asyncio, logging

from aiogram import Bot, Dispatcher
from config_data.config import load_config, Config
from handlers import other_handlers, user_handlers
from keyboards.set_menu import set_main_menu

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    
    # информация о запуске
    logger.info('запустился')

    # конфиг
    config: Config = load_config()

    # бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # сброс меню
    await set_main_menu(bot)

    # роутеры
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # удаление адейтов и start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
 
if __name__ == '__main__':
    asyncio.run(main())




