from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base, engine


class Hoge(Base):
    """
    hogeモデル
    """

    __tablename__ = "hoge"
    __table_args__ = {"comment": "hogeテーブル"}

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    name = Column("name", String(255), nullable=False, comment="名前")
    number = Column("number", Integer, nullable=False, comment="数値")
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
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        comment="更新日時",
    )


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
