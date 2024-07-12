from datetime import datetime

from sqlalchemy.orm import Session

from discord_memo.db.models import (
    Message,
    MessageGroup,
    Tag,
    Tag2Message,
    BinaryData,
    ImageLink,
)

from discord_memo.db.database import SessionLocal


# TagのCRUD操作
def create_tag(db: Session, channel_id: int, name: str):
    db_tag = Tag(channel_id=channel_id, name=name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tag(db: Session, tag_id: int):
    return (
        db.query(Tag).filter(Tag.channel_id == tag_id, Tag.is_deleted == False).first()
    )


def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tag).filter(Tag.is_deleted == False).offset(skip).limit(limit).all()


def update_tag(db: Session, tag_id: int, name: str):
    db_tag = (
        db.query(Tag).filter(Tag.channel_id == tag_id, Tag.is_deleted == False).first()
    )
    if db_tag:
        db_tag.name = name
        db_tag.updated_at = datetime.now()
        db.commit()
        db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: int):
    db_tag = db.query(Tag).filter(Tag.channel_id == tag_id).first()
    if db_tag:
        db_tag.is_deleted = True
        db.commit()
    return db_tag


# MessageのCRUD操作
def create_message(
    db: Session,
    content: str,
    message_link: str,
    binary_data_list: list,
    image_links_list: list,
):
    db_message = Message(content=content, message_link=message_link)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    for binary_data in binary_data_list:
        db_binary_data = BinaryData(
            message_id=db_message.id, is_binary_data=binary_data
        )
        db.add(db_binary_data)

    for link in image_links_list:
        db_image_link = ImageLink(message_id=db_message.id, image_link=link)
        db.add(db_image_link)

    db.commit()
    return db_message


def get_message(db: Session, message_id: int):
    return (
        db.query(Message)
        .filter(Message.id == message_id, Message.is_deleted == False)
        .first()
    )


def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Message)
        .filter(Message.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_message(
    db: Session,
    message_id: int,
    content: str = None,
    message_link: str = None,
    binary_data_list: list = None,
    image_links_list: list = None,
):
    db_message = (
        db.query(Message)
        .filter(Message.id == message_id, Message.is_deleted == False)
        .first()
    )
    if db_message:
        if content is not None:
            db_message.content = content
        if message_link is not None:
            db_message.message_link = message_link
        db_message.last_updated_at = datetime.now()

        if binary_data_list is not None:
            db.query(BinaryData).filter(BinaryData.message_id == message_id).delete()
            for binary_data in binary_data_list:
                db_binary_data = BinaryData(
                    message_id=message_id, is_binary_data=binary_data
                )
                db.add(db_binary_data)

        if image_links_list is not None:
            db.query(ImageLink).filter(ImageLink.message_id == message_id).delete()
            for link in image_links_list:
                db_image_link = ImageLink(message_id=message_id, image_link=link)
                db.add(db_image_link)

        db.commit()
        db.refresh(db_message)
    return db_message


def delete_message(db: Session, message_id: int):
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message:
        db_message.is_deleted = True
        db.commit()
    return db_message


# Tag2MessageのCRUD操作
def create_tag2message(
    db: Session, tag_id: int, message_id: int, channel_id: int, group_id: int = 0
):
    db_tag2message = Tag2Message(
        tag_id=tag_id, message_id=message_id, channel_id=channel_id, group_id=group_id
    )
    db.add(db_tag2message)
    db.commit()
    db.refresh(db_tag2message)
    return db_tag2message


def get_tag2message(db: Session, tag2message_id: int):
    return db.query(Tag2Message).filter(Tag2Message.id == tag2message_id).first()


def get_tag2messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tag2Message).offset(skip).limit(limit).all()


def get_tags_by_name(db: Session, name: str, skip: int = 0, limit: int = 100):
    return (
        db.query(Tag).filter(Tag.name.like(f"%{name}%")).offset(skip).limit(limit).all()
    )


def delete_tag2message(db: Session, tag2message_id: int):
    db_tag2message = (
        db.query(Tag2Message).filter(Tag2Message.id == tag2message_id).first()
    )
    if db_tag2message:
        db.delete(db_tag2message)
        db.commit()
    return db_tag2message


# MessageGroupのCRUD操作
def create_message_group(db: Session, message_id: int):
    db_message_group = MessageGroup(message_id=message_id)
    db.add(db_message_group)
    db.commit()
    db.refresh(db_message_group)
    return db_message_group


def add_to_message_group(db: Session, message_id: int, group_id: int):
    db_message_group = MessageGroup(message_id=message_id, group_id=group_id)
    db.add(db_message_group)
    db.commit()
    db.refresh(db_message_group)
    return db_message_group


def get_message_group(db: Session, group_id: int):
    return db.query(MessageGroup).filter(MessageGroup.group_id == group_id).first()


def get_message_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MessageGroup).offset(skip).limit(limit).all()


def delete_message_group(db: Session, group_id: int):
    db_message_group = (
        db.query(MessageGroup).filter(MessageGroup.group_id == group_id).first()
    )
    if db_message_group:
        db.delete(db_message_group)
        db.commit()
    return db_message_group
