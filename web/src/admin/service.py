from fastapi import FastAPI
from sqladmin import Admin

from src.admin.auth import authentication_backend
from src.admin.views.role import RoleAdmin
from src.db.sessions import engine, async_session_factory

def init_admin(app: FastAPI) -> None:
    """
    Инициализирует и монтирует админ-панель SQLAdmin.
    """
    admin = Admin(
        app=app,
        engine=engine,
        templates_dir="templates",
        base_url="/admin",
        title="Админ панель",
        debug=True,
        session_maker=async_session_factory,
        authentication_backend=authentication_backend
    )

    admin.add_view(RoleAdmin)
