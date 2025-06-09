from sqlalchemy import Boolean, String, Text, func, TIMESTAMP, ARRAY, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_class import Base


class BaseService(Base):
    """
    Модель для таблицы 'base_services'.
    Хранит общие свойства для всех типов услуг.
    """
    __tablename__ = "base_services"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Основная информация
    name: Mapped[str] = mapped_column(String(255))
    subtitle: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)

    # Используем тип ARRAY для хранения списка характеристик
    features: Mapped[list[str] | None] = mapped_column(ARRAY(String))

    # Финансовая информация
    currency: Mapped[str] = mapped_column(String(3), default="RUB", server_default="RUB")

    # Мета-информация
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")
    image_url: Mapped[str | None] = mapped_column(String(255))
    display_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    # --- Поля для наследования и интеграции с платежной системой ---

    # Это поле-дискриминатор. Оно будет говорить SQLAlchemy, с какой
    # дочерней таблицей (one_time_service_details или subscription_service_details)
    # связана эта запись.
    service_type: Mapped[str] = mapped_column(String(50))

    # Поля для чеков (согласно ФЗ-54)
    tax_type: Mapped[str] = mapped_column(String(20), default="none", server_default="none")
    payment_method_type: Mapped[str] = mapped_column(
        String(50), default="full_prepayment", server_default="full_prepayment"
    )
    payment_object_type: Mapped[str] = mapped_column(
        String(50), default="service", server_default="service"
    )

    # Временные метки
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Специальный атрибут для настройки наследования в SQLAlchemy
    __mapper_args__ = {
        "polymorphic_on": "service_type",
    }

    # --- Связи ---
    # Новая связь: услуга может быть рекомендована во многих квизах
    quiz_recommendations: Mapped[list["QuizSession"]] = relationship(
        back_populates="recommended_service"
    )
    # Новая связь: услуга может быть во многих заказах
    orders: Mapped[list["Order"]] = relationship(back_populates="service")

    # Новая связь: на одну услугу может быть много подписок
    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="service"
    )

    def __repr__(self) -> str:
        return f"<BaseService(id={self.id}, name='{self.name}')>"