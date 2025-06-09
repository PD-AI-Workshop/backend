from model.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column


class File(Base):
    name: Mapped[str]
    url: Mapped[str]
    size: Mapped[int]
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"))

    article: Mapped["Article"] = relationship(
        back_populates="files",
    )
