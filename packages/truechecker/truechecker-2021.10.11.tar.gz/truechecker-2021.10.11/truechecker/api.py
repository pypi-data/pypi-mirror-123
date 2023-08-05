"""True Checker API client module."""

import io
from pathlib import Path
from typing import Optional, Union

from aiohttp import ClientTimeout

from .base import BaseClient
from .const import HTTPMethods
from .models import CheckJob, Profile


class TrueChecker(BaseClient):
    """
    True Checker API client.

    Consists of API methods only.
    All other methods are hidden in the BaseClient.
    """

    API_VERSION = "1.1.0"
    API_HOST = "https://checker.trueweb.app/api"
    API_DOCS = "https://checker.trueweb.app/redoc"

    def __init__(
        self,
        token: Optional[str] = None,
        api_host: Optional[str] = None,
        timeout: Optional[ClientTimeout] = None,
    ):
        """
        Init True Checker API client.

        :param token: Telegram bot token
        :param api_host: API host url (optional)
        :param timeout: set session timeout, default is None
        """
        super().__init__(timeout=timeout)
        self.__token = token
        self._api_host = api_host or self.API_HOST

    async def check_profile(
        self,
        file: Union[str, Path, io.IOBase],
        token: Optional[str] = None,
        delay: Optional[float] = None,
    ) -> CheckJob:
        """
        Init new bot checking.

        :param token: Telegram bot token
        :param file: Any format of user_id array (csv, one-per-line or
            other). Telegram IDs will be parsed via regexp, so don't
            provide other digits looks like an telegram chat ID.
        :param delay: Delay between typing requests
        :return: new job object
        """
        token = token or self.__token
        if token is None:
            RuntimeError(
                "Please provide `token` for `TrueChecker` instance "
                "or pass it as a `check_profile` request param."
            )
        method = HTTPMethods.PUT
        url = f"{self._api_host}/profile/{token}"
        form = self._prepare_form(file)

        params = {}
        if delay is not None:
            params["delay"] = delay

        data = await self._make_request(method, url, params=params, data=form)
        return CheckJob(**data)

    async def get_profile(self, username: str) -> Profile:
        """
        Return checked bot profile on success.

        :param username: Bot username. Case insensitive
        :return: bot profile object or not found exception
        """
        method = HTTPMethods.GET
        url = f"{self._api_host}/profile/{username}"

        data = await self._make_request(method, url)
        return Profile(**data)

    async def get_job_status(self, job_id: str) -> CheckJob:
        """
        Find job by id and return job status.

        :param job_id: Job ID received after `check_profile` method
        :return: job object or not found exception
        """
        method = HTTPMethods.GET
        url = f"{self._api_host}/job/{job_id}"

        data = await self._make_request(method, url)
        return CheckJob(**data)

    async def cancel_job(self, job_id: str) -> CheckJob:
        """
        Cancel running Job.

        Job will stop with minor delay.
        (it may continue working for some additional seconds)

        :param job_id: Job ID received after `check_profile` method
        :return: job object / not found / not running
        """
        method = HTTPMethods.DELETE
        url = f"{self._api_host}/job/{job_id}"

        data = await self._make_request(method, url)
        return CheckJob(**data)
