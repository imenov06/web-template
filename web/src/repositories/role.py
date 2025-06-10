from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.role import Role
from src.schemas.role import RoleCreate, RoleUpdate
from .base import BaseRepository


class RoleRepository(BaseRepository[Role, RoleCreate, RoleUpdate]):
    """
    Репозиторий для работы с моделью Role.
    Наследует все базовые CRUD-операции от BaseRepository.
    """

    async def get_by_name(self, db: AsyncSession, *, name: str) -> Role | None:
        """
        Получение роли по имени.
        """
        statement = select(self.model).where(self.model.name == name)
        result = await db.execute(statement)
        return result.scalar_one_or_none()


# Создаем единственный экземпляр репозитория,
# который будет использоваться во всем приложении.
repository_role = RoleRepository(Role)