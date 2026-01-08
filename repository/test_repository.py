from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from model.category import Category
from model.article_to_category import article_category
from model.article_to_file import article_to_file
from model.article import Article
from model.file import File
from model.user import User

from settings import settings


class TestRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def cleanup_test_db(self) -> None:
        """Очищает все тестовые данные из базы"""
        try:
            await self._cleanup_via_models()
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    async def _cleanup_via_models(self) -> None:
        delete_users_except_admin_query = delete(User).where(User.email != settings.ADMIN_EMAIL)
        await self.session.execute(delete(File))
        await self.session.execute(delete(article_to_file))
        await self.session.execute(delete(Article))
        await self.session.execute(delete(article_category))
        await self.session.execute(delete(Category))
        await self.session.execute(delete_users_except_admin_query)

    async def cleanup_test_users(self) -> None:
        try:
            await self.session.execute(delete(User))
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
