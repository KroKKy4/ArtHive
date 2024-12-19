from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from db.models import (
    Image,
    Tag,
    ImageTag,
    User,
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
        """
        Создает новый пост (запись в таблице images) с указанными тегами.

        Аргументы:
            user_id (int): ID пользователя, который создает пост.
            image_data (bytes): Байтовые данные изображения.
            description (str): Описание к изображению.
            tags (List[str]): Список тегов для поста.
            created_at (datetime): Время создания поста. Если не указано, берется текущее время.

        Возвращает:
            Image: Созданный объект `Image` со связанными тегами.
        """
        if created_at is None:
            created_at = datetime.utcnow()

        # Проверим, что пользователь существует
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"Пользователь с id={user_id} не существует.")

        # Создаем запись в таблице images
        new_image = Image(
            user_id=user_id,
            image_data=image_data,
            description=description,
            created_at=created_at,
        )
        self.db.add(new_image)
        self.db.commit()
        self.db.refresh(new_image)

        # Обрабатываем и добавляем теги
        self._add_tags_to_image(new_image, tags)

        return new_image

    def _add_tags_to_image(self, image: Image, tags: List[str]):
        """
        Вспомогательный метод для добавления тегов к изображению.

        Аргументы:
            image (Image): Объект изображения, к которому нужно добавить теги.
            tags (List[str]): Список названий тегов.
        """
        normalized_tags = [t.strip() for t in tags if t.strip()]
        for tag_name in normalized_tags:
            tag = self._get_or_create_tag(tag_name)
            self._create_image_tag_relation(image, tag)

        self.db.commit()

    def _get_or_create_tag(self, tag_name: str) -> Tag:
        """
        Возвращает существующий тег по имени или создает новый, если такого нет.

        Аргументы:
            tag_name (str): Название тега.

        Возвращает:
            Tag: Объект тега из базы данных.
        """
        tag = self.db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            self.db.add(tag)
            self.db.commit()
            self.db.refresh(tag)
        return tag

    def _create_image_tag_relation(self, image: Image, tag: Tag):
        """
        Создает связь между изображением и тегом в таблице image_tags.

        Аргументы:
            image (Image): Объект изображения.
            tag (Tag): Объект тега.
        """
        # Проверим, не существует ли уже связь (на случай дублирования)
        exists = (
            self.db.query(ImageTag).filter_by(image_id=image.id, tag_id=tag.id).first()
        )

        if not exists:
            image_tag = ImageTag(image_id=image.id, tag_id=tag.id)
            self.db.add(image_tag)
