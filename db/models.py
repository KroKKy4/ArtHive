from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    LargeBinary,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    avatar = Column(LargeBinary, nullable=True)

    # Отношение к сохранённым постам через промежуточную таблицу
    saved_posts = relationship("SavedPost", back_populates="user")


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=True)
    image_data = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime)
    user = relationship("User", backref="images")

    # Отношение к тегам через ImageTag
    tags = relationship("ImageTag", back_populates="image")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    images = relationship("ImageTag", back_populates="tag")


class ImageTag(Base):
    __tablename__ = "image_tags"
    image_id = Column(Integer, ForeignKey("images.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    image = relationship("Image", back_populates="tags")
    tag = relationship("Tag", back_populates="images")


class SavedPost(Base):
    __tablename__ = "saved_posts"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    image_id = Column(Integer, ForeignKey("images.id"), primary_key=True)

    # Дополнительный уникальный индекс на пару (user_id, image_id)
    # чтобы один и тот же пост нельзя было сохранить несколько раз одним и тем же пользователем
    __table_args__ = (UniqueConstraint("user_id", "image_id", name="uq_user_image"),)

    user = relationship("User", back_populates="saved_posts")
    image = relationship("Image", backref="saved_by_users")
