from dataclasses import dataclass
from typing import List


@dataclass
class FileEntryData:
    is_binary_data: bool
    image_link: str


@dataclass
class MessageData:
    message_id: int
    content: str
    message_link: str
    file_entries: List[FileEntryData] | None = None
