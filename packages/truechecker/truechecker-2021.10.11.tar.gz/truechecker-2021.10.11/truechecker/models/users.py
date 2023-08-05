"""Pydantic model represents Telegram bot users statistics."""

from pydantic import BaseModel


class Users(BaseModel):  # pylint: disable=too-few-public-methods
    """Telegram bot users statistics model (part of Profile)."""

    active: int
    stopped: int
    deleted: int
    not_found: int
