from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from src.db.models.blog_post import BlogPostStatus
from .admin_user import AdminUserReadSimple


# --- Базовая схема с полями, которые заполняет пользователь ---
class BlogPostBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    slug: str = Field(..., min_length=3, max_length=255)
    content: str | None = None
    image_url: str | None = None


# --- Схема для валидации формы создания статьи ---
class BlogPostCreate(BlogPostBase):
    pass


# --- Схема для валидации формы обновления статьи ---
# Все поля опциональные. Статус тоже можно поменять.
class BlogPostUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=255)
    slug: str | None = Field(None, min_length=3, max_length=255)
    content: str | None = None
    image_url: str | None = None
    status: BlogPostStatus | None = None


# --- Схема для безопасной передачи данных статьи в шаблон ---
class BlogPostRead(BlogPostBase):
    id: int
    status: BlogPostStatus
    created_at: datetime
    published_at: datetime | None = None

    # Вкладываем упрощенную схему автора
    author: AdminUserReadSimple

    model_config = ConfigDict(from_attributes=True)