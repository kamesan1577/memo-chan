from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from discord_memo.db.database import Base, engine


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
        comment="更新日時",
    )
    is_deleted = Column("is_deleted", Boolean, nullable=False, default=False, comment="削除フラグ")

class Message(Base):
    __tablename__ = "message"
    __table_args__ = {"comment": "messageテーブル"}

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    is_binary_data = Column("is_binary_data", Boolean, nullable=False, comment="Isバイナリデータ")
    image_link = Column("image_link", String(255), nullable=True, comment="画像リンク")
    last_updated_at = Column(
        "last_updated_at",
        DateTime,
        nullable=False,
        server_default=func.now(),
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
    message_link = Column("message_link", String(255), nullable=True, comment="メッセージリンク")
    is_deleted = Column("is_deleted", Boolean, nullable=False, default=False, comment="削除フラグ")

    tags = relationship("Tag", secondary="tag2message", backref="messages")

class Tag2Message(Base):
    __tablename__ = "tag2message"
    __table_args__ = {"comment": "tag2messageテーブル"}

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    tag_id = Column("tag_id", Integer, ForeignKey("tag.id"), nullable=False, comment="タグID")
    message_id = Column("message_id", Integer, ForeignKey("message.id"), nullable=False, comment="メッセージID")
    channel_id = Column("channel_id", Integer, nullable=False, comment="チャンネルID")
    group_id = Column("group_id", Integer, nullable=False, default=0, comment="グループID")

class MessageGroup(Base):
    __tablename__ = "message_group"
    __table_args__ = {"comment": "message_groupテーブル"}

    group_id = Column("group_id", Integer, primary_key=True, index=True, autoincrement=True)
    message_id = Column("message_id", Integer, ForeignKey("message.id"), nullable=False, comment="メッセージID")
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
        comment="更新日時",
    )

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
