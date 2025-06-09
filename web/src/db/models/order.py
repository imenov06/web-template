# web/src/db/models/order.py

from sqlalchemy import (
    DECIMAL,
    ForeignKey,
    Integer,
    String,
    func,
    TIMESTAMP,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_class import Base


class Order(Base):
    """
    Модель для заказов, сделанных клиентами.
    """
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Внешние ключи
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.id"))
    service_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_services.id"))
    promo_code_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("promo_codes.id")
    )
    quiz_session_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("quiz_sessions.id"), unique=True
    )

    # Статус и сумма
    order_status: Mapped[str] = mapped_column(String(50), default="pending_payment")
    total_amount: Mapped[float] = mapped_column(DECIMAL(10, 2))
    currency: Mapped[str] = mapped_column(String(3), default="RUB")

    # Информация от платежной системы
    payment_gateway: Mapped[str | None] = mapped_column(String(50))
    gateway_invoice_id: Mapped[str | None] = mapped_column(String(255), unique=True)
    payment_transaction_id: Mapped[str | None] = mapped_column(String(255), unique=True)

    # Временные метки
    invoice_expires_at: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))
    paid_at: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # --- Связи ---
    customer: Mapped["Customer"] = relationship(back_populates="orders")
    service: Mapped["BaseService"] = relationship(back_populates="orders")
    promo_code: Mapped["PromoCode | None"] = relationship(back_populates="orders")
    quiz_session: Mapped["QuizSession | None"] = relationship(back_populates="order")

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, status='{self.order_status}')>"