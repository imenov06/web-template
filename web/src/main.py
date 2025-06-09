import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status

# Импортируем наши настройки
from src.core.config import settings

# Импортируем экземпляры bot и dp, а также функции для управления веб-хуком
from src.bot.main_bot import bot, dp, on_startup_webhook, on_shutdown_webhook

# Импортируем роутер для веб-хука Telegram
from src.bot import webhook_router

# Настройка базового логирования (можно расширить и настроить более детально)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Асинхронный менеджер контекста для управления событиями
    запуска и остановки приложения FastAPI.
    """
    logger.info("Application startup...")
    # При старте приложения устанавливаем веб-хук
    try:
        await on_startup_webhook()
    except Exception as e:
        # Если веб-хук не установился, это может быть критично.
        # Логируем и, возможно, приложение не должно стартовать корректно.
        # FastAPI может продолжить работать, но бот не будет получать обновления.
        logger.critical(f"CRITICAL: Webhook setup failed during startup: {e}", exc_info=True)
        # Можно здесь решить, нужно ли прерывать запуск приложения, если вебхук не установился.
        # Например, raise SystemExit("Webhook setup failed, exiting.")
        # Но это остановит FastAPI. Пока просто логируем как критическую ошибку.

    # Передаем управление приложению
    yield

    # Действия при остановке приложения (например, по Ctrl+C или при остановке Docker контейнера)
    logger.info("Application shutdown...")
    # Удаляем веб-хук
    await on_shutdown_webhook()
    # Закрываем сессию бота (в Aiogram 3+ это важно для корректного завершения)
    logger.info("Closing bot session...")
    await bot.session.close()
    logger.info("Bot session closed.")


# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="My FastAPI and Aiogram Bot Application",
    version="0.1.0",
    lifespan=lifespan # Подключаем менеджер жизненного цикла
)

# Сохраняем экземпляры bot и dp в состоянии приложения (app.state).
# Это позволит получить к ним доступ из других частей приложения,
# например, из обработчиков запросов (как в webhook_router.py через request.app.state).
app.state.bot = bot
app.state.dp = dp

# Подключаем роутер для веб-хука Telegram.
# Все запросы, приходящие на путь, указанный в settings.WEBHOOK_PATH,
# будут обрабатываться этим роутером.
app.include_router(webhook_router.router) # Префикс здесь не нужен, т.к. путь уже полный в WEBHOOK_PATH

# Пример простого эндпоинта для проверки, что FastAPI работает
@app.get("/")
async def root():
    return {"message": "FastAPI application is running. Bot webhook should be active."}
