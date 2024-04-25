import re
from fastapi import HTTPException
from app.core.db import SessionLocal
from app.db_models.chats import Chat, Tag, User, Image

def get_current_user_id() -> int:
    return 0


MAX_TAG_LENGTH = 64


def validate_tags(tags: list[str]) -> None:
    for tag in tags:
        if len(tag) == 0 or len(tag) > MAX_TAG_LENGTH:
            raise HTTPException(400, f'Length of tag \'{tag}\' should be in range [1 .. {MAX_TAG_LENGTH}]')
        if re.fullmatch('[a-zA-Z][a-zA-Z0-9\\-]*[a-zA-Z0-9]', tag) is None:
            raise HTTPException(400, f'Tag \'{tag}\' does not match the format')


def check_user_account_status(user_id: int) -> None:
    with SessionLocal() as session:
        with session.begin():
            user = session.query(User).filter_by(id=user_id).first()
            if user is None:
                raise HTTPException(403, f'User is not logged in / does not exist')

            if user_id == -1:
                raise HTTPException(403, f'User does not have permission to create chats')


def check_image_exists(image_id: int) -> None:
    with SessionLocal() as session:
        with session.begin():
            image = session.query(Image).filter_by(id=image_id).first()
            if image is None:
                raise HTTPException(400, f'Image is not uploaded to images storage')