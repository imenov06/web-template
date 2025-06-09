from sqlalchemy import String, func, TIMESTAMP, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base_class import Base


class PageContent(Base):
    """
    Модель для хранения редактируемого контента на страницах сайта.
    Каждая запись - это отдельный блок на определенной странице.
    """
    __tablename__ = "page_content"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Название страницы, к которой относится блок (например, 'home', 'about')
    page_name: Mapped[str] = mapped_column(String(100), index=True)

    # Уникальный идентификатор блока на странице (например, 'hero_title', 'features_list')
    block_name: Mapped[str] = mapped_column(String(100))

    # Содержимое блока в формате JSON, что позволяет хранить любую структуру
    content: Mapped[dict | list | None] = mapped_column(JSONB)

    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        # Гарантирует, что на одной странице не может быть двух блоков с одинаковым именем
        UniqueConstraint("page_name", "block_name", name="uq_page_block"),
    )

    def __repr__(self) -> str:
        return f"<PageContent(page='{self.page_name}', block='{self.block_name}')>"