import sqlite3
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    LargeBinary,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    avatar = Column(LargeBinary, nullable=True)


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=True)
    image_data = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime)
    user = relationship("User", backref="images")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class ImageTag(Base):
    __tablename__ = "image_tags"
    image_id = Column(Integer, ForeignKey("images.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    image = relationship("Image", backref="tags")
    tag = relationship("Tag", backref="images")


# Функция для создания таблиц (выполнять один раз)
def create_tables(engine):
    Base.metadata.create_all(engine)
