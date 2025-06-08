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
            article = Article(**article_dict)

            if category_ids:
                stmt = select(Category).where(Category.id.in_(category_ids)).options(selectinload(Category.articles))
                result = await session.execute(stmt)
                categories = result.scalars().all()
                article.categories = categories

            session.add(article)
            await session.commit()

            stmt = select(Article).where(Article.id == article.id).options(selectinload(Article.categories))
            result = await session.execute(stmt)
            article = result.scalar_one()

            return article

    async def update(self, id: int, article_dict: dict) -> None:
        async with async_session_maker() as session:
            category_ids = article_dict.pop("category_ids", None)
            query = select(Article).options(selectinload(Article.categories)).where(Article.id == id)
            result = await session.execute(query)
            article = result.scalar_one_or_none()

            for key, value in article_dict.items():
                setattr(article, key, value)

            if category_ids:
                query = select(Category).where(Category.id.in_(category_ids))
                result = await session.execute(query)
                categories = result.scalars().all()
                article.categories = categories

            session.add(article)
            await session.commit()
            await session.refresh(article)
