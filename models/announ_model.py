from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import String, DATETIME


class Base(DeclarativeBase):
    pass


class Annoucement(Base):
    __tablename__ = "announcement"
    announcement_id: Mapped[int] = mapped_column(primary_key=True)
    owner: Mapped[str] = mapped_column(String())
    date: Mapped[datetime] = mapped_column(DATETIME())
    status: Mapped[str] = mapped_column(String())
    breed: Mapped[str] = mapped_column(String())
    nickname: Mapped[str] = mapped_column(String())
    gender: Mapped[str] = mapped_column(String())
    features: Mapped[str] = mapped_column(String())
    details: Mapped[str] = mapped_column(String())
    animal_type: Mapped[str] = mapped_column(String())
    photo: Mapped[str] = mapped_column(String())
    completion_date: Mapped[datetime] = mapped_column(DATETIME())

