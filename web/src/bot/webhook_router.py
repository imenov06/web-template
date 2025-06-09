import logging
from fastapi import APIRouter, Request, HTTPException, Header, Response, status
from aiogram.types import Update

from src.core.config import settings


router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    settings.WEBHOOK_PATH,
    include_in_schema=False
)
async def telegram_webhook(
    request: Request,
    update_data: dict,
    x_telegram_bot_api_secret_token: str | None = Header(None)
):
    """
    Этот эндпоинт принимает обновления от Telegram в формате JSON.
    """
    if settings.WEBHOOK_SECRET:
        if not x_telegram_bot_api_secret_token:
            logger.warning("Secret token header missing")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Secret token missing")
        if x_telegram_bot_api_secret_token != settings.WEBHOOK_SECRET:
            logger.warning("Invalid secret token received")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid secret token")


    try:
        bot_instance = request.app.state.bot
        dispatcher_instance = request.app.state.dp
    except AttributeError:
        logger.error("Bot or Dispatcher not found in app.state. Ensure they are set during FastAPI startup.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Bot not configured")

    if not bot_instance or not dispatcher_instance:
        logger.error("Bot or Dispatcher instance is None in app.state.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Bot not configured (instance is None)")

    telegram_update = Update(**update_data)
    logger.debug(f"Received update ID: {telegram_update.update_id} of type: {telegram_update.event_type}")

    try:
        await dispatcher_instance.feed_webhook_update(bot=bot_instance, update=telegram_update)
    except Exception as e:
        pass

    return Response(status_code=status.HTTP_200_OK)
