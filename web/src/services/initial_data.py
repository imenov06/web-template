from src.core.config import settings
from src.db.sessions import async_session_factory
from src.repositories.admin_user import repository_admin_user
from src.repositories.role import repository_role
from src.schemas.admin_user import AdminUserCreate
from src.schemas.role import RoleCreate


async def create_first_user() -> None:
    """
    Основная асинхронная функция для инициализации данных.
    """
    async with async_session_factory() as db:

        # --- 1. Создание роли администратора ---
        admin_role_name = "Главный администратор"
        role = await repository_role.get_by_name(db, name=admin_role_name)

        if not role:
            role_in = RoleCreate(
                name=admin_role_name,
                description="Полный доступ ко всем разделам админ-панели."
            )
            role = await repository_role.create(db, obj_in=role_in)

        user = await repository_admin_user.get_by_username(
            db, username=settings.FIRST_SUPERUSER_LOGIN
        )

        if not user:
            user_in = AdminUserCreate(
                username=settings.FIRST_SUPERUSER_LOGIN,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                role_id=role.id,
                is_active=True,
            )
            user = await repository_admin_user.create(db, obj_in=user_in)


