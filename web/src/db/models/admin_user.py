# web/src/db/models/admin_user.py

from sqlalchemy import Boolean, ForeignKey, Integer, String, func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_class import Base


class AdminUser(Base):
    """
    Модель для пользователей админ-панели (администраторы, менеджеры и т.д.).
    """
    __tablename__ = "admin_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    # Это поле будет хранить не сам пароль, а его безопасный хэш.
    password_hash: Mapped[str] = mapped_column(String(255))

    full_name: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255), unique=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login_at: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))

    # Внешний ключ, связывающий пользователя с его ролью.
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"))

    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    role: Mapped["Role"] = relationship(back_populates="admin_users")

    handled_submissions: Mapped[list["ContactFormSubmission"]] = relationship(
        back_populates="replied_by_admin"
    )

    # Связь со статьями: один администратор может быть автором многих статей
    blog_posts: Mapped[list["BlogPost"]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"<AdminUser(id={self.id}, username='{self.username}')>"