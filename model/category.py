from model.base import Base
from sqlalchemy.orm import Mapped, relationship
from model.article_to_category import article_category


class Category(Base):
    name: Mapped[str]

    articles: Mapped[list["Article"]] = relationship("Article", secondary=article_category, back_populates="categories")
