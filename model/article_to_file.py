from model.base import Base
from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint

article_to_file = Table(
    "article_to_file",
    Base.metadata,
    Column("article_id", ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
    Column("file_id", ForeignKey("files.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("file_id", name="uq_file_article"),
)
