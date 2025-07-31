from model.base import Base
from enums.role import Role
from fastapi import Depends
from db.session import async_session_maker
from typing import AsyncGenerator, Optional
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase


class User(Base, SQLAlchemyBaseUserTable[int]):
    username: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str] = mapped_column(ENUM(Role, name="role", create_type=False), default=Role.USER)

    articles: Mapped[list["Article"]] = relationship(
        "Article", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
