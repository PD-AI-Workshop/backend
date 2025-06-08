from model.base import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column


class Article(Base):
    title: Mapped[str]
    created_date: Mapped[datetime] = mapped_column(default=datetime.now())
    time_reading: Mapped[int]
    main_image_url: Mapped[str]
    text_id: Mapped[int]
    text: None
    user_id: Mapped[int]
    user: None
