from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    text,
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from discord_memo.db.database import Base, engine

# 中間テーブルの定義
tag2messagegroup = Table(
    "tag2messagegroup",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("tag_id", Integer, ForeignKey("tag.id"), nullable=False, comment="タグID"),
    Column(
        "message_group_id",
        Integer,
        ForeignKey("message_group.group_id"),
        nullable=False,
        comment="メッセージグループID",
    ),
)


class Tag(Base):
    __tablename__ = "tag"
    __table_args__ = {"comment": "tagテーブル"}

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    channel_id = Column("channel_id", Integer, nullable=False, comment="チャンネルID")
    name = Column("name", String(255), nullable=False, comment="タグ名")
    created_at = Column(
        "created_at",
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment="作成日時",
    )
    updated_at = Column(
        "updated_at",
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新日時",
    )
    is_deleted = Column(
        "is_deleted", Boolean, nullable=False, default=False, comment="削除フラグ"
    )
    message_groups = relationship(
        "MessageGroup", secondary=tag2messagegroup, back_populates="tags"
    )


class Message(Base):
    __tablename__ = "message"
    __table_args__ = {"comment": "messageテーブル"}

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    message_id = Column(
        "message_id",
        Integer,
        nullable=False,
        comment="メッセージID",
    )
    last_updated_at = Column(
        "last_updated_at",
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="最終更新日時",
    )
    created_at = Column(
        "created_at",
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment="作成日時",
    )
    content = Column("content", Text, nullable=True, comment="メッセージのText")
    message_link = Column(
        "message_link", String(255), nullable=True, comment="メッセージリンク"
    )
    is_deleted = Column(
        "is_deleted", Boolean, nullable=False, default=False, comment="削除フラグ"
    )
    group_id = Column(Integer, ForeignKey("message_group.group_id"))
    group = relationship("MessageGroup", back_populates="messages")
    file_entries = relationship("FileEntry", back_populates="message")


class FileEntry(Base):
    __tablename__ = "file_entry"
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    message_table_id = Column(
        "message_id", Integer, ForeignKey("message.id"), nullable=False
    )
    is_binary_data = Column(
        "is_binary_data", Boolean, nullable=False, comment="Isバイナリデータ"
    )
    image_link = Column("image_link", String(255), nullable=True, comment="画像リンク")
    message = relationship("Message", back_populates="file_entries")


class MessageGroup(Base):
    __tablename__ = "message_group"
    __table_args__ = {"comment": "message_groupテーブル"}

    group_id = Column(
        "group_id", Integer, primary_key=True, index=True, autoincrement=True
    )
    created_at = Column(
        "created_at",
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment="作成日時",
    )
    updated_at = Column(
        "updated_at",
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新日時",
    )
    is_deleted = Column(
        "is_deleted", Boolean, nullable=False, default=False, comment="削除フラグ"
    )
    messages = relationship("Message", back_populates="group")
    tags = relationship(
        "Tag", secondary=tag2messagegroup, back_populates="message_groups"
    )


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
