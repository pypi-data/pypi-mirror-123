"""
Helps to use ujson module instead of json module.

If ujson is installed the app will use it. To prevent using installed
ujson you should use DISABLE_UJSON environment variable.
More about ujson: https://github.com/ultrajson/ultrajson

If ujson is not installed the app will use basic json module.
"""
import os

disabled = os.getenv("DISABLE_UJSON")
if not disabled:
    try:
        import ujson as json
    except ImportError:  # pragma: no cover
        import json  # type: ignore
else:  # pragma: no cover
    import json  # type: ignore


def loads(data) -> dict:
    """Load a JSON to a dict via available JSON converter."""
    return json.loads(data)


def dumps(data) -> str:  # pragma: no cover
    """Dump a data to JSON via available JSON converter."""
    return json.dumps(data, ensure_ascii=False)
