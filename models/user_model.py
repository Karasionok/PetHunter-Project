from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    pass


class User(Base, UserMixin):
    __tablename__ = "user"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String())
    login: Mapped[str] = mapped_column(String())
    password: Mapped[str] = mapped_column(String())
    phone: Mapped[str] = mapped_column(String())
    district: Mapped[str] = mapped_column(String())

    def get_id(self):
        return self.user_id