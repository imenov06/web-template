from sqlalchemy import DECIMAL, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base_service import BaseService


class OneTimeServiceDetails(BaseService):
    """
    Модель для деталей разовых услуг.
    Наследует все поля от BaseService и добавляет свои.
    """
    __tablename__ = "one_time_service_details"

    # Это поле одновременно и первичный ключ для этой таблицы,
    # и внешний ключ, ссылающийся на родительскую таблицу.
    service_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("base_services.id"), primary_key=True
    )

    # --- Поля, специфичные только для разовых услуг ---
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    duration_days: Mapped[int | None] = mapped_column(Integer)

    delivery_type: Mapped[str | None] = mapped_column(String(50))
    delivery_content: Mapped[str | None] = mapped_column(Text)

    # --- Настройка наследования ---
    # Этот аргумент говорит SQLAlchemy, что когда в родительской таблице
    # в поле 'service_type' стоит значение 'one_time',
    # то нужно работать с этим классом.
    __mapper_args__ = {
        "polymorphic_identity": "one_time",
    }

    def __repr__(self) -> str:
        return f"<OneTimeServiceDetails(service_id={self.service_id}, price={self.price})>"