from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel


class Note(BaseModel):
    path: Path
    title: str
    frontmatter: dict[str, Any]
    body: str


class VaultError(Exception):
    pass


def split_frontmatter(note_text: str) -> tuple[dict[str, Any], str]:
    parts = note_text.splitlines()
    if not parts or parts[0].strip() != "---":
        return {}, note_text

    end = None
    for i, line in enumerate(parts[1:], start=1):
        if line.strip() == "---":
            end = i
            break

    if end is None:
        return {}, note_text

    frontmatter = "\n".join(parts[1:end])
    try:
        data = yaml.safe_load(frontmatter)
        if data is None:
            data = {}
        if not isinstance(data, dict):
            return {}, note_text
    except yaml.YAMLError:
        return {}, note_text

    body = "\n".join(parts[end+1:])
    return data, body
