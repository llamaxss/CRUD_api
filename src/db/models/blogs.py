from sqlalchemy.orm import Mapped, mapped_column
import datetime
from dataclasses import dataclass, field

from ..base import Base


@dataclass
class BlogSchema:
    title: str
    content: str
    last_modified: datetime.datetime = field(init=False)

    def __post_init__(self):
        self.last_modified = datetime.datetime.now()


class BlogDb(Base):
    __tablename__ = "blog"

    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column()
    last_modified: Mapped[datetime.datetime] = mapped_column()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at,
            "last_modified": self.last_modified,
        }

    def __repr__(self) -> str:
        return f"Blog(id={self.id}, title={self.title}, content={self.content}, created_at={self.created_at}, last_modified={self.last_modified})"
