"""Pydantic model represents Telegram bot profile."""

from datetime import datetime

from pydantic import BaseModel

from .users import Users


class Profile(BaseModel):  # pylint: disable=too-few-public-methods
    """Telegram bot profile model."""

    username: str
    full_name: str
    updated: datetime
    users: Users
