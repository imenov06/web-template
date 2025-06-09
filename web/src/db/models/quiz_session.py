from sqlalchemy import BigInteger, ForeignKey, Integer, func, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_class import Base


class QuizSession(Base):
    """
    Модель для сессий прохождения квиза пользователями Telegram.
    """
    __tablename__ = "quiz_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)

    telegram_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("telegram_users.telegram_id")
    )
    # Поле для хранения ответов пользователя в формате JSON
    responses: Mapped[dict | list | None] = mapped_column(JSONB)

    recommended_service_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("base_services.id")
    )

    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    completed_at: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))

    # --- Связи ---
    telegram_user: Mapped["TelegramUser"] = relationship(
        back_populates="quiz_sessions"
    )
    recommended_service: Mapped["BaseService | None"] = relationship(
        back_populates="quiz_recommendations"
    )

    # Связь "один-к-одному" с заказом
    order: Mapped["Order | None"] = relationship(back_populates="quiz_session")

    def __repr__(self) -> str:
        return f"<QuizSession(id={self.id}, user_id={self.telegram_user_id})>"