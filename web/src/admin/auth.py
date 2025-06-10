from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.core.config import settings
from src.db.sessions import async_session_factory
from src.repositories.admin_user import repository_admin_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        """
        Обрабатывает попытку входа в систему.
        """
        form = await request.form()
        username, password = form["username"], form["password"]

        async with async_session_factory() as db:
            user = await repository_admin_user.authenticate(
                db=db, username=username, password=password
            )

        if user:

            request.session.update({"admin_user_id": user.id, "username": user.username})

        return user is not None

    async def logout(self, request: Request) -> bool:
        """
        Обрабатывает выход из системы.
        """
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """
        Проверяет, аутентифицирован ли пользователь.
        Вызывается при каждом запросе к админ-панели.
        """
        # Просто проверяем, есть ли наш ключ в сессии
        return "admin_user_id" in request.session



authentication_backend = AdminAuth(secret_key=settings.ADMIN_SECRET_KEY)
