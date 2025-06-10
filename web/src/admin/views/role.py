from sqladmin import ModelView

from src.db.models.role import Role


class RoleAdmin(ModelView, model=Role):
    """
    Представление для управления Ролями в админ-панели.
    """
    column_list = [Role.id, Role.name, Role.permissions]

    name = "Роль"
    name_plural = "Роли"

    # Иконка для меню (из FontAwesome)
    icon = "fa-solid fa-user-shield"