from src.db.models.blog_post import BlogPost
from src.schemas.blog_post import BlogPostCreate, BlogPostUpdate
from .base import BaseRepository


class BlogPostRepository(BaseRepository[BlogPost, BlogPostCreate, BlogPostUpdate]):
    """
    Репозиторий для работы с моделью BlogPost.
    Наследует все базовые CRUD-операции от BaseRepository.
    Здесь можно будет добавлять специфичные для блога методы,
    например, 'найти все опубликованные статьи'.
    """
    pass


# Создаем единственный экземпляр репозитория
repository_blog_post = BlogPostRepository(BlogPost)