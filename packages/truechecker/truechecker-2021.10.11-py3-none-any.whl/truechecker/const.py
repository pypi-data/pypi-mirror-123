"""Constant dataclasses."""

from enum import Enum


class HTTPMethods(str, Enum):
    """Available HTTP methods."""

    PUT = "PUT"
    GET = "GET"
    DELETE = "DELETE"
