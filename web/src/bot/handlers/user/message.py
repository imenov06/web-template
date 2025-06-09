from aiogram import Router, types
from aiogram.filters import CommandStart, Command

# Создаем новый роутер для этих хэндлеров
router = Router(name="common-handlers")


@router.message(CommandStart())
async def handle_start(message: types.Message):
    """
    Этот хэндлер будет вызываться при получении команды /start.
    """
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f"Привет, {user_name} (ID: {user_id})! 👋\nЯ твой новый бот, запущенный через FastAPI и Docker."

    # Пример использования HTML разметки, так как мы указали parse_mode=ParseMode.HTML
    # в main_bot.py
    # text += "\n\n<b>Это жирный текст.</b> <i>Это курсив.</i>"
    # text += "\n<a href='https://core.telegram.org/bots/api'>Ссылка на API Telegram</a>"
    # text += "\n<code>Это моноширинный текст (код)</code>"
    # text += "\n<pre>Это блок предварительно отформатированного текста (для блоков кода)</pre>"

    await message.answer(text)


@router.message(Command(commands=["help"]))
async def handle_help(message: types.Message):
    """
    Этот хэндлер будет вызываться при получении команды /help.
    """
    text = (
        "Я пока мало что умею, но вот список доступных команд:\n"
        "/start - Начать диалог\n"
        "/help - Получить эту справку"
        # Добавляйте сюда описание других команд по мере их появления
    )
    await message.answer(text)

# Вы можете добавить здесь другие общие хэндлеры
# Например, обработчик для всех текстовых сообщений, которые не являются командами:
# @router.message()
# async def handle_all_text(message: types.Message):
#     await message.reply(f"Ты написал: {message.text}")
