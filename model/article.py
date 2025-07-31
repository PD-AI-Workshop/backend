from model.base import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from model.article_to_file import article_to_file
from model.article_to_category import article_category
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Article(Base):
    title: Mapped[str]
    created_date: Mapped[datetime] = mapped_column(default=datetime.now)
    time_reading: Mapped[int]
    main_image_url: Mapped[str]
    text_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="articles", lazy="selectin")

    categories: Mapped[list["Category"]] = relationship(
        "Category", secondary=article_category, back_populates="articles", lazy="selectin"
    )

    files: Mapped[list["File"]] = relationship(
        "File", secondary=article_to_file, lazy="selectin", cascade="all, delete"
    )

    @property
    def category_ids(self) -> list[int]:
        return [c.id for c in self.categories]

    @property
    def image_ids(self) -> list[int]:
        return [f.id for f in self.files] if self.files else []
