from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.models import (
    Image,
    Tag,
    ImageTag,
    User,
    SavedPost,  # Импортируем новую модель
)


class PostsCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_image_with_tags(
        self,
        user_id: int,
        image_data: bytes,
        description: Optional[str],
        tags: List[str],
        created_at: Optional[datetime] = None,
    ) -> Image:
        if created_at is None:
            created_at = datetime.utcnow()

        # Проверим, что пользователь существует
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"Пользователь с id={user_id} не существует.")

        new_image = Image(
            user_id=user_id,
            image_data=image_data,
            description=description,
            created_at=created_at,
        )
        self.db.add(new_image)
        self.db.commit()
        self.db.refresh(new_image)

        self._add_tags_to_image(new_image, tags)

        return new_image

    def _add_tags_to_image(self, image: Image, tags: List[str]):
        normalized_tags = [t.strip() for t in tags if t.strip()]
        for tag_name in normalized_tags:
            tag = self._get_or_create_tag(tag_name)
            self._create_image_tag_relation(image, tag)

        self.db.commit()

    def _get_or_create_tag(self, tag_name: str) -> Tag:
        tag = self.db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            self.db.add(tag)
            self.db.commit()
            self.db.refresh(tag)
        return tag

    def _create_image_tag_relation(self, image: Image, tag: Tag):
        exists = (
            self.db.query(ImageTag).filter_by(image_id=image.id, tag_id=tag.id).first()
        )

        if not exists:
            image_tag = ImageTag(image_id=image.id, tag_id=tag.id)
            self.db.add(image_tag)

    def get_user_images(self, user_id: int) -> List[Image]:
        images = (
            self.db.query(Image)
            .filter(Image.user_id == user_id)
            .order_by(Image.created_at.desc())
            .all()
        )
        return images  # type: ignore

    def get_all_images(self) -> List[Image]:
        images = self.db.query(Image).order_by(Image.created_at.desc()).all()
        return images  # type: ignore

    def search_posts_by_tags(self, tag_name: str):
        posts = (
            self.db.query(Image)
            .join(ImageTag, Image.id == ImageTag.image_id)  # type: ignore
            .join(Tag, ImageTag.tag_id == Tag.id)
            .filter(Tag.name.ilike(f"%{tag_name}%"))
            .order_by(Image.created_at.desc())
            .all()
        )
        return posts

    def save_post_for_user(self, user_id: int, image_id: int):
        # Проверим, что пользователь и пост существуют
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"Пользователь с id={user_id} не найден.")

        image = self.db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise ValueError(f"Пост с id={image_id} не найден.")

        saved = SavedPost(user_id=user_id, image_id=image_id)
        self.db.add(saved)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            # Значит пост уже сохранён данным пользователем
            raise ValueError("Этот пост уже сохранён пользователем")

    def get_saved_posts_for_user(self, user_id: int) -> List[Image]:
        # Получаем список постов, сохранённых пользователем
        # Можно сделать через подзапрос или простой join
        posts = (
            self.db.query(Image)
            .join(SavedPost, Image.id == SavedPost.image_id)  # type: ignore
            .filter(SavedPost.user_id == user_id)
            .order_by(Image.created_at.desc())
            .all()
        )
        return posts
