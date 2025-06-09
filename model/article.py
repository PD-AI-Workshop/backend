from model.base import Base
from datetime import datetime
from model.article_to_category import article_category
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Article(Base):
    title: Mapped[str]
    created_date: Mapped[datetime] = mapped_column(default=datetime.now())
    time_reading: Mapped[int]
    main_image_url: Mapped[str]
    text_id: Mapped[int]
    user_id: Mapped[int]
    user: None

    categories: Mapped[list["Category"]] = relationship(
        "Category", secondary=article_category, back_populates="articles"
    )

    files: Mapped[list["File"]] = relationship("File", back_populates="article", cascade="all, delete-orphan")

    @property
    def category_ids(self) -> list[int]:
        return [c.id for c in self.categories]
