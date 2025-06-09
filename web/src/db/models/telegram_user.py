from sqlalchemy import BigInteger, Boolean, String, func, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_class import Base


class TelegramUser(Base):
    """
    Модель пользователя Telegram-бота.
    """
    __tablename__ = "telegram_users"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=False
    )

    username: Mapped[str | None] = mapped_column(String(255))
    first_name: Mapped[str | None] = mapped_column(String(255))
    last_name: Mapped[str | None] = mapped_column(String(255))
    language_code: Mapped[str | None] = mapped_column(String(10))
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)

    bot_state: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    last_interaction_at: Mapped[str | None] = mapped_column(
        TIMESTAMP(timezone=True)
    )
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    # --- Связи ---
    customer: Mapped["Customer | None"] = relationship(back_populates="telegram_user")

    # Новая связь: у одного пользователя может быть много сессий квиза
    quiz_sessions: Mapped[list["QuizSession"]] = relationship(back_populates="telegram_user")

    def __repr__(self) -> str:
        """
        Возвращает однозначное представление объекта для разработчика.
        """
        return f"<TelegramUser(id={self.telegram_id}, username='{self.username}')>"