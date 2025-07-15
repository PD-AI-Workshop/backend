from typing import Optional
from model.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column


class File(Base):
    name: Mapped[str]
    url: Mapped[str]
    size: Mapped[int]
    article_id: Mapped[Optional[int]] = mapped_column(ForeignKey("articles.id"), nullable=True)

    article: Mapped["Article"] = relationship(
        back_populates="files",
        foreign_keys=article_id,
    )
