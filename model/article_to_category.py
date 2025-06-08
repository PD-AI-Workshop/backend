from model.base import Base
from sqlalchemy import Column, ForeignKey, Table


article_category = Table(
    "article_category",
    Base.metadata,
    Column("article_id", ForeignKey("articles.id"), primary_key=True),
    Column("category_id", ForeignKey("categorys.id"), primary_key=True),
)
