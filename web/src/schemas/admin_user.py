from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .role import RoleRead


# --- Базовая схема с общими полями ---
class AdminUserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    full_name: str | None = None
    email: EmailStr | None = None
    is_active: bool = True


# --- Схема для создания нового администратора ---
# Используется для валидации данных из формы.
class AdminUserCreate(AdminUserBase):
    # Пароль требуется только при создании, и его нет в других схемах.
    password: str = Field(..., min_length=8)
    role_id: int


# --- Схема для обновления администратора ---
# Все поля опциональные.
class AdminUserUpdate(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=100)
    full_name: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None
    password: str | None = Field(None, min_length=8)
    role_id: int | None = None


# --- Схема для чтения данных об администраторе ---
# Безопасная схема для передачи данных в шаблоны.
class AdminUserRead(AdminUserBase):
    id: int

    # Вложенная схема: при чтении администратора мы также
    # подгрузим и отобразим полную информацию о его роли.
    role: RoleRead

    model_config = ConfigDict(from_attributes=True)


class AdminUserReadSimple(BaseModel):
    id: int
    full_name: str | None = None

    model_config = ConfigDict(from_attributes=True)