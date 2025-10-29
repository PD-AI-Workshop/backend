from model.base import Base
from sqlalchemy.orm import Mapped


class File(Base):
    name: Mapped[str]
    url: Mapped[str]
    size: Mapped[int]
