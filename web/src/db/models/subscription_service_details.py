from sqlalchemy import DECIMAL, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base_service import BaseService


class SubscriptionServiceDetails(BaseService):
    """
    Модель для деталей подписных услуг.
    Наследует все поля от BaseService и добавляет свои.
    """
    __tablename__ = "subscription_service_details"

    service_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("base_services.id"), primary_key=True
    )

    # --- Поля, специфичные только для подписных услуг ---
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    billing_cycle_months: Mapped[int] = mapped_column(Integer, default=1)

    # --- Настройка наследования ---
    # Указываем 'subscription' как идентификатор для этого типа услуг
    __mapper_args__ = {
        "polymorphic_identity": "subscription",
    }

    def __repr__(self) -> str:
        return f"<SubscriptionServiceDetails(service_id={self.service_id}, price={self.price})>"