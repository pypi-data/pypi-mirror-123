"""
Python client library for True Checker API.

Repository: https://gitlab.com/true-web-app/true-checker/true-checker-python
API docs: https://checker.trueweb.app/redoc
"""

__all__ = ["TrueChecker"]

import os

from .api import TrueChecker

# install uvloop if exists and not disabled
try:
    import uvloop  # noqa
except ImportError:  # pragma: no cover
    pass
else:
    if "DISABLE_UVLOOP" not in os.environ:
        uvloop.install()
