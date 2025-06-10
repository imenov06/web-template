import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from src.admin.service import admin, init_admin
from src.core.config import settings

from src.bot.main_bot import bot, dp, on_startup_webhook, on_shutdown_webhook

from src.bot import webhook_router
from src.services.initial_data import create_first_user

from src.web_pages.routers_user.index import router as index_router

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
    try:
        await on_startup_webhook()
        await create_first_user()
        logger.info("Initial data check complete.")
    except Exception as e:
        logger.critical(f"CRITICAL: Webhook setup failed during startup: {e}", exc_info=True)


    yield

    logger.info("Application shutdown...")
    await on_shutdown_webhook()
    logger.info("Closing bot session...")
    await bot.session.close()
    logger.info("Bot session closed.")


app = FastAPI(
    title="My FastAPI and Aiogram Bot Application",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
)

app.state.bot = bot
app.state.dp = dp

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")
init_admin(app=app)

app.include_router(webhook_router.router)
app.include_router(index_router)
