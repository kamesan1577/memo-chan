from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from discord_memo.db.models import (
    Message,
    MessageGroup,
    Tag,
    tag2messagegroup,
    FileEntry,
    NodeMessage,
)

from discord_memo.db.database import SessionLocal
from discord_memo.db.schemas import MessageData, FileEntryData


# TagのCRUD操作
def create_tag(db: Session, channel_id: int, name: str):
    db_tag = Tag(channel_id=channel_id, name=name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tag(db: Session, channel_id: int):
    return (
        db.query(Tag)
        .filter(Tag.channel_id == channel_id, Tag.is_deleted == False)
        .first()
    )


def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tag).filter(Tag.is_deleted == False).offset(skip).limit(limit).all()


def update_tag(db: Session, channel_id: int, name: str):
    db_tag = (
        db.query(Tag)
        .filter(Tag.channel_id == channel_id, Tag.is_deleted == False)
        .first()
    )
    if db_tag:
        db_tag.name = name
        db_tag.updated_at = datetime.now()
        db.commit()
        db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, channel_id: int):
    db_tag = db.query(Tag).filter(Tag.channel_id == channel_id).first()
    if db_tag:
        db_tag.is_deleted = True
        db.commit()
    return db_tag


def get_tags_by_name(db: Session, name: str, skip: int = 0, limit: int = 100):
    return (
        db.query(Tag)
        .filter(Tag.name == name, Tag.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


# MessageGroupのCRUD操作
def create_message_group(
    db: Session, message_list: List[MessageData], tag_id_list: List[int]
):
    db_message_group = MessageGroup()
    db.add(db_message_group)
    db.commit()
    db.refresh(db_message_group)

    for message in message_list:
        db_message = _create_message(
            db,
            message,
        )
        db_message_group.messages.append(db_message)
        db.add(db_message_group)
    for tag_id in tag_id_list:
        _add_tag_to_message_group(db, tag_id, int(db_message_group.group_id))

    db.commit()
    db.refresh(db_message_group)
    return db_message_group


def get_message_group(db: Session, message_id: int):
    return (
        db.query(MessageGroup)
        .join(MessageGroup.messages)
        .filter(Message.message_id == message_id)
        .first()
    )


def get_message_groups(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(MessageGroup)
        .filter(MessageGroup.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_message_group(db: Session, message_id: int):
    db_message_group = (
        db.query(MessageGroup)
        .join(MessageGroup.messages)
        .filter(Message.message_id == message_id)
        .first()
    )
    if db_message_group:
        db_message_group.is_deleted = True
        db.commit()
    return db_message_group

def add_node_message(db: Session, message_id: int, group_id: int):
    db_node_message = NodeMessage(message_id=message_id, message_group_id=group_id)
    db.add(db_node_message)
    db.commit()
    db.refresh(db_node_message)
    return db_node_message


def _add_tag_to_message_group(db: Session, tag_id: int, group_id: int):
    stmt = tag2messagegroup.insert().values(tag_id=tag_id, message_group_id=group_id)
    db.execute(stmt)
    db.commit()


def _get_tags_for_message_group(db: Session, group_id: int):
    stmt = tag2messagegroup.select().where(tag2messagegroup.c.group_id == group_id)
    return db.execute(stmt).fetchall()


def _remove_tag_from_message_group(db: Session, tag_id: int, message_id: int):
    stmt = tag2messagegroup.delete().where(
        tag2messagegroup.c.tag_id == tag_id
        and tag2messagegroup.c.group_id == message_id
    )
    db.execute(stmt)
    db.commit()


# MessageのCRUD操作
def _create_message(db: Session, message: MessageData):
    db_message = Message(
        message_id=message.message_id,
        content=message.content,
        message_link=message.message_link,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    if message.file_entries:
        for entry in message.file_entries:
            db_file_entry = FileEntry(
                message_table_id=db_message.id,
                is_binary_data=entry.is_binary_data,
                image_link=entry.image_link,
            )
            db.add(db_file_entry)

        db.commit()

    return db_message


def _get_message(db: Session, message_id: int):
    return (
        db.query(Message)
        .filter(Message.message_id == message_id, Message.is_deleted == False)
        .first()
    )


def _get_messages(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Message)
        .filter(Message.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def _update_message(
    db: Session,
    message: MessageData,
):
    db_message = (
        db.query(Message)
        .filter(Message.message_id == message.message_id, Message.is_deleted == False)
        .first()
    )
    if db_message:
        if message.content is not None:
            db_message.content = message.content
        if message.message_link is not None:
            db_message.message_link = message.message_link
        db_message.last_updated_at = datetime.now()

        if message.file_entries is not None:
            db.query(FileEntry).filter(FileEntry.message_id == db_message.id).delete()
            for entry in message.file_entries:
                db_file_entry = FileEntry(
                    message_table_id=db_message.id,
                    is_binary_data=entry.is_binary_data,
                    image_link=entry.image_link,
                )
                db.add(db_file_entry)

        db.commit()
        db.refresh(db_message)
    return db_message


def _delete_message(db: Session, message_id: int):
    db_message = db.query(Message).filter(Message.message_id == message_id).first()
    if db_message:
        db_message.is_deleted = True
        db.commit()
    return db_message
