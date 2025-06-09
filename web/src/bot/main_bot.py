import logging
from aiogram import Bot, Dispatcher, enums
from aiogram.client.default import DefaultBotProperties
# from aiogram.fsm.storage.memory import MemoryStorage # Если понадобится FSM

from web.src.core.config import settings
# Импорты хэндлеров будут здесь, когда мы их создадим
from src.bot.handlers.user.message import router

logger = logging.getLogger(__name__)

# Инициализация FSM хранилища (если нужно)
# fsm_storage = MemoryStorage()

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=enums.ParseMode.HTML)
)

# dp = Dispatcher(storage=fsm_storage) # Если используете FSM
dp = Dispatcher()

def setup_bot_routers():
    """Подключаем все роутеры к диспетчеру."""
    # Пример:
    dp.include_router(router)
    # dp.include_router(some_router_2.router)
    # Пока у нас нет хэндлеров, эта функция может быть пустой или отсутствовать.
    # Я оставлю ее как напоминание.
    pass

# Если у вас уже есть какие-то начальные роутеры, можно их подключить здесь
setup_bot_routers()


async def on_startup_webhook():
    """Вызывается при старте FastAPI для установки веб-хука."""
    logger.info("Executing on_startup_webhook...")
    webhook_url = settings.WEBHOOK_URL
    try:
        await bot.set_webhook(
            url=webhook_url,
            secret_token=settings.WEBHOOK_SECRET,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True
        )
        logger.info(f"Webhook set to: {webhook_url}")
    except Exception as e:
        logger.error(f"Error setting webhook to {webhook_url}: {e}", exc_info=True)
        # Возможно, стоит пробросить исключение дальше, чтобы старт приложения прервался,
        # если веб-хук критичен для работы. Или обработать по-другому.
        raise

async def on_shutdown_webhook():
    """Вызывается при остановке FastAPI для удаления веб-хука."""
    logger.info("Executing on_shutdown_webhook...")
    try:
        current_webhook_info = await bot.get_webhook_info()
        if current_webhook_info.url:
            await bot.delete_webhook(drop_pending_updates=True)
            logger.info(f"Webhook for {current_webhook_info.url} successfully deleted.")
        else:
            logger.info("No active webhook to delete.")
    except Exception as e:
        logger.error(f"Error deleting webhook: {e}", exc_info=True)

