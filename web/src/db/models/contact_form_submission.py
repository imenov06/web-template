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


class SubmissionStatus(str, enum.Enum):
    """Статусы заявок с форм обратной связи."""
    new = "new"
    read = "read"
    replied = "replied"
    archived = "archived"


class ContactFormSubmission(Base):
    """
    Модель для хранения заявок, отправленных через формы на сайте.
    """
    __tablename__ = "contact_form_submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(255))
    contact_method: Mapped[str] = mapped_column(String(50))
    contact_data: Mapped[str] = mapped_column(String(255))
    subject: Mapped[str | None] = mapped_column(String(255))
    message: Mapped[str | None] = mapped_column(Text)

    status: Mapped[SubmissionStatus] = mapped_column(
        SAEnum(SubmissionStatus), default=SubmissionStatus.new
    )

    submitted_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    ip_address: Mapped[str | None] = mapped_column(String(45))
    page_submitted_from: Mapped[str | None] = mapped_column(String(255))

    replied_by_admin_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("admin_users.id")
    )
    replied_at: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))
    notes: Mapped[str | None] = mapped_column(Text)

    # --- Связи ---
    replied_by_admin: Mapped["AdminUser | None"] = relationship(
        back_populates="handled_submissions"
    )

    def __repr__(self) -> str:
        return f"<ContactFormSubmission(id={self.id}, status='{self.status.value}')>"