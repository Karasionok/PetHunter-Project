from sqlalchemy import *
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    district = Column(String, nullable=False)


class Announcement(Base):
    __tablename__ = 'announcement'

    announcement_id = Column(Integer, primary_key=True)
    owner = Column(ForeignKey('user.user_id'), nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(Numeric, nullable=False)
    breed = Column(Numeric)
    nickname = Column(Numeric)
    gender = Column(Numeric)
    features = Column(Text)
    details = Column(Text)
    animal_type = Column(Numeric)
    photo = Column(Numeric)
    completion_date = Column(DateTime)

    user = relationship('User')


class Marker(Base):
    __tablename__ = 'marker'

    marker_id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    place = Column(Numeric)
    announcement = Column(ForeignKey('announcement.announcement_id'))

    announcement1 = relationship('Announcement')
