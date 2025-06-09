import enum

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Text,
    TIMESTAMP,
    Enum as SAEnum,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_class import Base


class BlogPostStatus(str, enum.Enum):
    """Статусы записей в блоге."""
    draft = "draft"
    published = "published"
    archived = "archived"


class BlogPost(Base):
    """
    Модель для записей в блоге (статей).
    """
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    content: Mapped[str | None] = mapped_column(Text)

    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("admin_users.id"))

    status: Mapped[BlogPostStatus] = mapped_column(
        SAEnum(BlogPostStatus), default=BlogPostStatus.draft, server_default="draft"
    )
    published_at: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))
    image_url: Mapped[str | None] = mapped_column(String(255))

    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # --- Связи ---
    author: Mapped["AdminUser"] = relationship(back_populates="blog_posts")

    def __repr__(self) -> str:
        return f"<BlogPost(id={self.id}, title='{self.title}')>"