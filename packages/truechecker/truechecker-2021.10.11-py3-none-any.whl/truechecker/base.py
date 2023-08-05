"""Base aiohttp client class module."""

import asyncio
import io
import ssl
from pathlib import Path
from typing import Any, Dict, Optional, Union

import certifi
from aiohttp import (
    ClientSession,
    ClientTimeout,
    ContentTypeError,
    FormData,
    TCPConnector,
)
from aiohttp.typedefs import StrOrURL

from .exceptions import (
    BadRequest,
    BadState,
    NotFound,
    TrueCheckerException,
    Unauthorized,
    ValidationError,
)
from .utils import json

EXC_MAPPING = {
    400: BadRequest,
    401: Unauthorized,
    404: NotFound,
    409: BadState,
    422: ValidationError,
}


class BaseClient:
    """
    Base aiohttp client.

    Consists of all methods need to make a request to API:
     - session caching
     - request wrapping
     - exceptions wrapping
     - grace session close
     - e.t.c.
    """

    def __init__(self, timeout: Optional[ClientTimeout] = None):
        """
        Set defaults on object init.

        By default `self._session` is None.
        It will be created on a first API request.
        The second request will use the same `self._session`.
        """
        self._timeout = timeout or ClientTimeout(total=0)
        self._session: Optional[ClientSession] = None

    def get_session(self):
        """Get cached session. One session per instance."""
        if isinstance(self._session, ClientSession) and not self._session.closed:
            return self._session

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = TCPConnector(ssl=ssl_context)

        self._session = ClientSession(
            connector=connector,
            json_serialize=json.dumps,
            timeout=self._timeout,
        )
        return self._session

    async def _make_request(self, method: str, url: StrOrURL, **kwargs) -> dict:
        """
        Make a request.

        :param method: HTTP Method
        :param url: endpoint link
        :param kwargs: data, params, json and other...
        :return: status and result or exception
        """
        session = self.get_session()

        async with session.request(method, url, **kwargs) as response:
            status = response.status
            try:
                data = await response.json(loads=json.loads)
            except ContentTypeError:
                data = await response.text()

        if status != 200:
            raise self._process_exception(status, data)

        return data

    def _prepare_form(self, file: Union[str, Path, io.IOBase]) -> FormData:
        """Create form to pass file via multipart/form-data."""
        form = FormData()
        form.add_field("file", self._prepare_file(file))
        return form

    @staticmethod
    def _prepare_file(file: Union[str, Path, io.IOBase]):
        """Prepare accepted types to correct file type."""
        if isinstance(file, str):
            return Path(file).open("rb")

        if isinstance(file, io.IOBase):
            return file

        if isinstance(file, Path):
            return file.open("rb")

        raise TypeError(f"Not supported file type: `{type(file).__name__}`")

    @staticmethod
    def _process_exception(
        status: int, data: Union[Dict[str, Any], str]
    ) -> TrueCheckerException:
        """
        Wrap API exceptions.

        :param status: response status
        :param data: response json converted to dict()
        :return: wrapped exception
        """
        if isinstance(data, dict):
            text = data.get("message") or data.get("detail")
        else:
            text = data
        exc = EXC_MAPPING.get(status, TrueCheckerException)
        return exc(text)

    async def close(self):
        """Close the session graceful."""
        if not isinstance(self._session, ClientSession):
            return

        if self._session.closed:
            return

        await self._session.close()
        await asyncio.sleep(0.25)
