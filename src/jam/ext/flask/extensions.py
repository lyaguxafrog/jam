# -*- coding: utf-8 -*-

from typing import Any, Optional

from flask import Flask, g, request

from jam import Jam


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
        logger = self._jam._BaseJam__logger
        
        logger.debug("JWTExtension: Attempting to extract token from request")
        if self.cookie:
            token = request.cookies.get(self.cookie)
            if token:
                logger.debug(f"Token found in cookie '{self.cookie}'")

        if not token and self.header:
            header = request.headers.get(self.header)
            if header and header.startswith("Bearer "):
                token = header.split("Bearer ")[1]
                logger.debug(f"Token found in header '{self.header}'")

        if not token:
            logger.debug("No token found in request")
            return None
        
        logger.debug(f"Verifying JWT token (length: {len(token)} chars), check_list={self.__use_list}")
        try:
            payload: dict[str, Any] = self._jam.jwt_verify_token(
                token=token, check_exp=True, check_list=self.__use_list
            )
            logger.debug(f"JWT token verified successfully, payload keys: {list(payload.keys())}")
        except Exception as e:
            logger.warning(f"JWT token verification failed: {e}")
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
        logger = self._jam._BaseJam__logger
        
        logger.debug("SessionExtension: Attempting to extract session ID from request")
        if self.cookie:
            session_id = request.cookies.get(self.cookie)
            if session_id:
                logger.debug(f"Session ID found in cookie '{self.cookie}'")

        if not session_id and self.header:
            header = request.headers.get(self.header)
            if header and header.startswith("Bearer "):
                session_id = header.split("Bearer ")[1]
                logger.debug(f"Session ID found in header '{self.header}'")

        if not session_id:
            logger.debug("No session ID found in request")
            return None
        
        logger.debug(f"Getting session data for session ID: {session_id}")
        try:
            payload: Optional[dict[str, Any]] = self._jam.session_get(
                session_id
            )
            if payload:
                logger.debug(f"Session data retrieved successfully, keys: {list(payload.keys())}")
            else:
                logger.debug(f"Session {session_id} not found")
        except Exception as e:
            logger.warning(f"Session retrieval failed: {e}")
            return None

        g.payload = payload
        return payload

    def init_app(self, app: Flask) -> None:
        """Flask app init."""
        app.before_request(self._get_payload)
        app.extensions["jam"] = self._jam
