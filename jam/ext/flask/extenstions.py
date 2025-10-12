# -*- coding: utf-8 -*-

from typing import Any, Optional, Union

from flask import Flask, request

from jam import Jam
from jam.__logger__ import logger


class JamExtension:
    """Base jam extension.

    Simply adds instance jam to app.extensions.
    """

    def __init__(
        self,
        app: Optional[Flask] = None,
        config: Union[str, dict[str, Any]] = "pyproject.toml",
        pointer: str = "jam",
    ) -> None:
        """Constructor.

        Args:
            app (Flask | None): Flask app
            config (str | dict[str, Any]): Jam config
            pointer (str): Config pointer
        """
        self._jam = Jam(config, pointer)
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Flask app init."""
        app.extensions["jam"] = self._jam


class JWTExtension(JamExtension):
    """JWT extension fot flask."""

    def __init__(
        self,
        app: Optional[Flask] = None,
        config: Union[str, dict[str, Any]] = "pyproject.toml",
        pointer: str = "jam",
        header_name: Optional[str] = "Authorization",
        cookie_name: Optional[str] = None,
    ) -> None:
        """Constructor.

        Args:
            app (Flask | None): Flask app
            config (str | dict[str, Any]): Jam config
            pointer (str): Config pointer
            header_name (str | None): Header with access token
            cookie_name (str | None): Cookie with access token
        """
        super().__init__(app, config, pointer)
        self.__use_list = getattr(self._jam.module, "list", False)
        self.header = header_name
        self.cookie = cookie_name

    def _get_payload(self) -> Optional[dict[str, Any]]:
        token = None
        if self.cookie:
            token = request.cookies.get(self.cookie)

        if not token and self.header:
            header = request.headers.get(self.header)
            if header and header.startswith("Bearer "):
                token = header.split("Bearer ")[1]

        if not token:
            return None
        try:
            payload: dict[str, Any] = self._jam.verify_jwt_token(
                token=token, check_exp=True, check_list=self.__use_list
            )
        except Exception as e:
            logger.warning(str(e))
            return None

        return payload

    def init_app(self, app: Flask) -> None:
        """Flask app init."""
        app.before_request(self._get_payload)
        app.extensions["jam"] = self._jam
