# web/src/db/models/promo_code.py

import enum

from sqlalchemy import (
    DECIMAL,
    Boolean,
    Integer,
    String,
    TIMESTAMP,
    Enum as SAEnum,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_class import Base


class DiscountType(str, enum.Enum):
    """Типы скидок для промокодов."""
    fixed_amount = "fixed_amount"
    percentage = "percentage"


class PromoCode(Base):
    """
    Модель для промокодов на скидку.
    """
    __tablename__ = "promo_codes"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    # Указываем, что в БД это поле будет храниться как Enum
    discount_type: Mapped[DiscountType] = mapped_column(SAEnum(DiscountType))
    discount_value: Mapped[float] = mapped_column(DECIMAL(10, 2))

    expires_at: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))
    usage_limit: Mapped[int | None] = mapped_column(Integer)
    used_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")

    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Завершаем настройку двусторонней связи
    orders: Mapped[list["Order"]] = relationship(back_populates="promo_code")


    def __repr__(self) -> str:
        return f"<PromoCode(id={self.id}, code='{self.code}')>"