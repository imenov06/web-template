# web/src/repositories/base.py

from typing import Any, Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base_class import Base

# --- Дженерики и типы для репозитория ---
# Определяем тип для нашей модели SQLAlchemy
ModelType = TypeVar("ModelType", bound=Base)
# Определяем тип для схемы создания Pydantic
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# Определяем тип для схемы обновления Pydantic
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Базовый репозиторий с CRUD-операциями.

        :param model: SQLAlchemy модель.
        """
        self.model = model

    async def get(self, db: AsyncSession, *, obj_id: Any) -> ModelType | None:
        """Получение одной записи по ID."""
        statement = select(self.model).where(self.model.id == obj_id)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        """Получение списка записей с пагинацией."""
        statement = select(self.model).offset(skip).limit(limit)
        result = await db.execute(statement)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Создание новой записи."""
        # Преобразуем Pydantic схему в словарь
        obj_in_data = obj_in.model_dump()
        # Создаем экземпляр модели SQLAlchemy
        db_obj = self.model(**obj_in_data)
        # Добавляем в сессию и сохраняем в БД
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self, db: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType | dict
    ) -> ModelType:
        """Обновление существующей записи."""
        # Получаем данные для обновления в виде словаря
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        # Обновляем поля объекта
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, obj_id: int) -> ModelType | None:
        """Удаление записи по ID."""
        db_obj = await self.get(db, obj_id=obj_id)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
        return db_obj