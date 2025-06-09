# web/src/db/models/subscription.py

import enum

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    Enum as SAEnum,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_class import Base


class SubscriptionStatus(str, enum.Enum):
    """Статусы подписок."""
    active = "active"
    trial = "trial"
    past_due = "past_due"
    cancelled = "cancelled"
    expired = "expired"


class Subscription(Base):
    """
    Модель для подписок клиентов на рекуррентные услуги.
    """
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.id"))
    service_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_services.id"))

    status: Mapped[SubscriptionStatus] = mapped_column(SAEnum(SubscriptionStatus))

    current_period_start_date: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))
    current_period_end_date: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))
    cancelled_at: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))
    ended_at: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))

    payment_gateway_subscription_id: Mapped[str | None] = mapped_column(
        String(255), unique=True
    )
    auto_renew: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # --- Связи ---
    customer: Mapped["Customer"] = relationship(back_populates="subscriptions")
    service: Mapped["BaseService"] = relationship(back_populates="subscriptions")


    def __repr__(self) -> str:
        return f"<Subscription(id={self.id}, status='{self.status.value}')>"