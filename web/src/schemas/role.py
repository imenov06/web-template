from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# --- Базовая схема с общими полями ---
# Содержит поля, которые есть и при создании, и при чтении.
class RoleBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = None
    permissions: dict | list | None = None


# --- Схема для создания новой записи ---
# Используется для валидации данных из HTML-формы.
class RoleCreate(RoleBase):
    pass


# --- Схема для обновления записи ---
# Все поля опциональные, чтобы можно было обновить только часть данных.
class RoleUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = None
    permissions: dict | list | None = None


# --- Схема для чтения данных из БД ---
# Включает поля, которые генерируются базой данных (id, created_at и т.д.).
class RoleRead(RoleBase):
    id: int
    created_at: datetime

    # Эта настройка "разрешает" Pydantic создавать схему напрямую
    # из объекта модели SQLAlchemy (orm_mode в Pydantic v1).
    model_config = ConfigDict(from_attributes=True)