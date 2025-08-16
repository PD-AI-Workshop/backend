from model.base import Base
from sqlalchemy.orm import Mapped, relationship


class File(Base):
    name: Mapped[str]
    url: Mapped[str]
    size: Mapped[int]
