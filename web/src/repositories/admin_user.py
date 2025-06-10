from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import get_password_hash, verify_password
from src.db.models.admin_user import AdminUser
from src.schemas.admin_user import AdminUserCreate, AdminUserUpdate
from .base import BaseRepository


class AdminUserRepository(BaseRepository[AdminUser, AdminUserCreate, AdminUserUpdate]):
    """
    Репозиторий для работы с моделью AdminUser.
    """

    async def create(self, db: AsyncSession, *, obj_in: AdminUserCreate) -> AdminUser:
        """
        Создает нового администратора, хэшируя его пароль.
        """
        # Преобразуем Pydantic схему в словарь
        create_data = obj_in.model_dump()
        # Извлекаем пароль и удаляем его из словаря
        password = create_data.pop("password")
        # Хэшируем пароль
        hashed_password = get_password_hash(password)
        # Создаем экземпляр модели SQLAlchemy с хэшированным паролем
        db_obj = self.model(**create_data, password_hash=hashed_password)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self, db: AsyncSession, *, db_obj: AdminUser, obj_in: AdminUserUpdate
    ) -> AdminUser:
        """
        Обновляет администратора. Если в данных есть новый пароль,
        он будет захэширован.
        """
        update_data = obj_in.model_dump(exclude_unset=True)

        # Если в данных на обновление есть пароль
        if "password" in update_data and update_data["password"]:
            # Хэшируем новый пароль
            hashed_password = get_password_hash(update_data["password"])
            # Заменяем текстовый пароль на хэш
            update_data["password_hash"] = hashed_password
            del update_data["password"]

        # Вызываем метод update из базового репозитория с обновленными данными
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(
            self, db: AsyncSession, *, username: str, password: str
    ) -> AdminUser | None:
        """
        Аутентификация пользователя по имени пользователя и паролю.
        """
        # Находим пользователя по имени
        statement = select(self.model).where(self.model.username == username)
        result = await db.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            return None
        # Проверяем, совпадает ли введенный пароль с хэшем в базе
        if not verify_password(password, user.password_hash):
            return None

        return user

    async def get_by_username(
            self, db: AsyncSession, *, username: str
    ) -> AdminUser | None:
        """
        Получение администратора по имени пользователя (логину).
        """
        statement = select(self.model).where(self.model.username == username)
        result = await db.execute(statement)
        return result.scalar_one_or_none()


# Создаем единственный экземпляр репозитория
repository_admin_user = AdminUserRepository(AdminUser)