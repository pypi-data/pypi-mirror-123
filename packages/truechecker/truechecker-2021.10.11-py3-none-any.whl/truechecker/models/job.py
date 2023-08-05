"""Pydantic model represents True Checker API jobs."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class JobStates(str, Enum):
    """Available True Checker API job states."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"
    ERROR = "error"


class CheckJob(BaseModel):  # pylint: disable=too-few-public-methods
    """True Checker API job model."""

    id: str
    bot_id: int
    state: JobStates
    progress: float
    created: datetime
    description: Optional[str]
