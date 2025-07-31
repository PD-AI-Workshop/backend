from model.file import File
from sqlalchemy import select
from model.article import Article
from model.category import Category
from sqlalchemy.orm import selectinload
from db.session import async_session_maker
from repository.crud_base_repository import CRUDBaseRepository


class ArticleRepository(CRUDBaseRepository):
    model = Article

    async def create(self, article_dict: dict) -> Article:
        async with async_session_maker() as session:
            category_ids = article_dict.pop("category_ids", [])
            image_ids = article_dict.pop("image_ids", [])
            article = Article(**article_dict)

            if category_ids:
                stmt = select(Category).where(Category.id.in_(category_ids)).options(selectinload(Category.articles))
                result = await session.execute(stmt)
                categories = result.scalars().all()
                article.categories = categories

            if image_ids:
                stmt = select(File).where(File.id.in_(image_ids))
                result = await session.execute(stmt)
                files = result.scalars().all()
                article.files = files

            session.add(article)
            await session.commit()
            await session.refresh(article, ["categories", "files"])

            return article

    async def update(self, id: int, article_dict: dict) -> None:
        async with async_session_maker() as session:
            category_ids = article_dict.pop("category_ids", None)
            image_ids = article_dict.pop("image_ids", None)

            query = (
                select(Article)
                .options(selectinload(Article.categories), selectinload(Article.files))
                .where(Article.id == id)
            )

            result = await session.execute(query)
            article = result.scalar_one_or_none()

            for key, value in article_dict.items():
                setattr(article, key, value)

            if category_ids is not None:
                query = select(Category).where(Category.id.in_(category_ids))
                result = await session.execute(query)
                categories = result.scalars().all()
                article.categories = categories

            if image_ids is not None:
                query = select(File).where(File.id.in_(image_ids))
                result = await session.execute(query)
                files = result.scalars().all()
                article.files = files

            session.add(article)
            await session.commit()
            await session.refresh(article)
