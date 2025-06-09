from sqlalchemy import BigInteger, ForeignKey, String, func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_class import Base


class Customer(Base):
    """
    Модель клиента/покупателя на сайте.
    """
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String(255))
    phone_number: Mapped[str | None] = mapped_column(String(50))

    # Обновили ForeignKey, чтобы он ссылался на 'telegram_users.telegram_id'
    telegram_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("telegram_users.telegram_id"), unique=True
    )

    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    # --- Связи ---
    telegram_user: Mapped["TelegramUser | None"] = relationship(
        back_populates="customer"
    )

    # Новая связь: у одного клиента может быть много заказов
    orders: Mapped[list["Order"]] = relationship(back_populates="customer")

    # Новая связь: у одного клиента может быть много подписок
    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="customer"
    )

    def __repr__(self) -> str:
        return f"<Customer(id={self.id}, email='{self.email}')>"