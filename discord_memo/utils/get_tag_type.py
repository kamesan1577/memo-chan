import re
from typing import Literal


def get_tag_type(text: str) -> Literal["new_tag", "existing_tag", "invalid_tag"]:
    if re.match(r"<#\d+>", text):
        return "existing_tag"
    elif re.match(r"#.+", text):
        return "new_tag"
    else:
        return "invalid_tag"