from typing import List
from sqlalchemy.orm import Session
from discord_memo.db.database import SessionLocal, engine
from discord_memo.db import models, crud
from discord_memo.db.database import Base
from discord_memo.db.schemas import MessageData, FileEntryData


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    tags = [
        {"channel_id": 1, "name": "tag1"},
        {"channel_id": 2, "name": "tag2"},
        {"channel_id": 3, "name": "tag3"},
    ]

    for tag in tags:
        crud.create_tag(db, tag["channel_id"], tag["name"])

    messages: List[MessageData] = [
        MessageData(
            message_id=1,
            content="message1",
            message_link="https://discord.com/channels/1/1",
            file_entries=[
                FileEntryData(is_binary_data=False, image_link="https://example.com")
            ],
        ),
        MessageData(
            message_id=2,
            content="message2",
            message_link="https://discord.com/channels/1/2",
            file_entries=[
                FileEntryData(is_binary_data=False, image_link="https://example.com")
            ],
        ),
        MessageData(
            message_id=3,
            content="message3",
            message_link="https://discord.com/channels/1/3",
            file_entries=[
                FileEntryData(is_binary_data=False, image_link="https://example.com")
            ],
        ),
    ]
    message_groups = [
        {"message_list": messages, "tag_id_list": [1]},
        {
            "message_list": [
                MessageData(
                    message_id=4,
                    content="message4",
                    message_link="https://discord.com/channels/1/4",
                )
            ],
            "tag_id_list": [1, 2],
        },
    ]

    for message_group in message_groups:
        crud.create_message_group(
            db, message_group["message_list"], message_group["tag_id_list"]
        )

    db.close()
