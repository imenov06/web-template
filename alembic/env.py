# alembic/env.py

import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# --- 1. Настройка пути к исходному коду вашего проекта ---
# Это нужно, чтобы Alembic мог импортировать ваши модели и настройки.
# Мы добавляем папку 'web' в системный путь Python.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'web')))

# --- 2. Импорт моделей и настроек ---
# Импортируем базовый класс для моделей
from src.db.base_class import Base

# Импортируем ВСЕ ваши модели.
# так как только после импорта SQLAlchemy узнает о них.
from src.db.models.admin_user import AdminUser
from src.db.models.blog_post import BlogPost
from src.db.models.contact_form_submission import ContactFormSubmission
from src.db.models.customer import Customer
from src.db.models.order import Order
from src.db.models.page_content import PageContent
from src.db.models.promo_code import PromoCode
from src.db.models.quiz_session import QuizSession
from src.db.models.role import Role
from src.db.models.subscription import Subscription
from src.db.models.telegram_user import TelegramUser
from src.db.models.base_service import BaseService
from src.db.models.one_time_service_details import OneTimeServiceDetails
from src.db.models.subscription_service_details import SubscriptionServiceDetails

# Импортируем объект настроек вашего приложения
from src.core.config import settings


# --- Стандартная конфигурация Alembic ---
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- 3. Установка URL базы данных и цели для автогенерации ---
# Переопределяем URL из alembic.ini на тот, что в настройках вашего приложения
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Указываем Alembic, что наши модели описаны в Base.metadata
target_metadata = Base.metadata

# --- Функции для выполнения миграций ---
def run_migrations_offline() -> None:
    """Запускает миграции в 'оффлайн' режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запускает миграции в 'онлайн' режиме (асинхронно)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
