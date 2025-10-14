# -*- coding: utf-8 -*-

from typing import Any, Optional

from flask import Flask, g, request

from jam import Jam
from jam.__logger__ import logger


class JamExtension:
    """Base jam extension.

    Simply adds instance jam to app.extensions.
    """

    def __init__(
        self,
        jam: Jam,
        app: Optional[Flask] = None,
    ) -> None:
        """Constructor.

        Args:
            jam (jam): Jam instance
            app (Flask | None): Flask app
        """
        self._jam = jam
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Flask app init."""
        app.extensions["jam"] = self._jam


class JWTExtension(JamExtension):
    """JWT extension fot flask."""

    def __init__(
        self,
        jam: Jam,
        app: Optional[Flask] = None,
        header_name: Optional[str] = "Authorization",
        cookie_name: Optional[str] = None,
    ) -> None:
        """Constructor.

        Args:
            jam (Jam): Jam instance
            app (Flask | None): Flask app
            header_name (str | None): Header with access token
            cookie_name (str | None): Cookie with access token
        """
        super().__init__(jam, app)
        self.__use_list = getattr(self._jam.module, "list", False)
        self.header = header_name
        self.cookie = cookie_name

    def _get_payload(self) -> Optional[dict[str, Any]]:
        token = None
        g.payload = None
        if self.cookie:
            token = request.cookies.get(self.cookie)

        if not token and self.header:
            header = request.headers.get(self.header)
            if header and header.startswith("Bearer "):
                token = header.split("Bearer ")[1]

        if not token:
            return None
        try:
            payload: dict[str, Any] = self._jam.jwt_verify_token(
                token=token, check_exp=True, check_list=self.__use_list
            )
        except Exception as e:
            logger.warning(str(e))
            return None

        g.payload = payload
        return payload

    def init_app(self, app: Flask) -> None:
        """Flask app init."""
        app.before_request(self._get_payload)
        app.extensions["jam"] = self._jam


class SessionExtension(JamExtension):
    """Session extension for Jam."""

    def __init__(
        self,
        jam: Jam,
        app: Optional[Flask] = None,
        header_name: Optional[str] = None,
        cookie_name: Optional[str] = "sessionId",
    ) -> None:
        """Constructor.

        Args:
            jam (Jam): Jam instance
            app (Flask | None): Flask app
            header_name (str | None): Session id header
            cookie_name (str | None): Session id cookie
        """
        super().__init__(jam, app)
        self.header = header_name
        self.cookie = cookie_name

    def _get_payload(self) -> Optional[dict[str, Any]]:
        session_id = None
        g.payload = None
        if self.cookie:
            session_id = request.cookies.get(self.cookie)

        if not session_id and self.header:
            header = request.headers.get(self.header)
            if header and header.startswith("Bearer "):
                session_id = header.split("Bearer ")[1]

        if not session_id:
            return None
        try:
            payload: Optional[dict[str, Any]] = self._jam.session_get(
                session_id
            )
        except Exception as e:
            logger.warning(str(e))
            return None

        g.payload = payload
        return payload

    def init_app(self, app: Flask) -> None:
        """Flask app init."""
        app.before_request(self._get_payload)
        app.extensions["jam"] = self._jam
