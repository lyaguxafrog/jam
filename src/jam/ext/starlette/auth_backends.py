# -*- coding: utf-8 -*-

from typing import Any, Optional

from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    BaseUser,
)
from starlette.requests import HTTPConnection

from jam.__base__ import BaseJam
from jam.utils.await_maybe import await_maybe

from .value import Payload


class JWTBackend(AuthenticationBackend):
    """JWT Backend for Starlette AuthenticationMiddleware."""

    def __init__(
        self,
        jam: BaseJam,
        cookie_name: Optional[str] = None,
        header_name: Optional[str] = "Authorization",
    ) -> None:
        """Constructor.

        Args:
            jam (BaseJam): Jam instance
            cookie_name (str | None): Access token cookie name
            header_name (str | None): Access token header name
        """
        self._jam = jam
        self.cookie_name = cookie_name
        self.header_name = header_name
        self.__use_list = getattr(self._jam.module, "list", False)

    async def authenticate(
        self, conn: HTTPConnection
    ) -> Optional[tuple[AuthCredentials, BaseUser]]:
        """Starlette authentication handler."""
        logger = self._jam._BaseJam__logger
        token = None

        logger.debug("JWTBackend: Attempting to extract token from request")
        if self.cookie_name:
            token = conn.cookies.get(self.cookie_name)
            if token:
                logger.debug(f"Token found in cookie '{self.cookie_name}'")

        if not token and self.header_name:
            header = conn.headers.get(self.header_name)
            if header and header.startswith("Bearer "):
                token = header.split("Bearer ")[1]
                logger.debug(f"Token found in header '{self.header_name}'")

        if not token:
            logger.debug("No token found in request")
            return None

        logger.debug(f"Verifying JWT token (length: {len(token)} chars), check_list={self.__use_list}")
        try:
            payload: dict[str, Any] = await await_maybe(
                self._jam.jwt_verify_token(
                    token=token, check_exp=True, check_list=self.__use_list
                )
            )
            logger.debug(f"JWT token verified successfully, payload keys: {list(payload.keys())}")
        except Exception as e:
            logger.warning(f"Token verify error: {e}")
            raise AuthenticationError("Token verification failed.")

        return AuthCredentials(["authenticated"]), Payload(payload=payload)


class SessionBackend(AuthenticationBackend):
    """Sessions backend for starlette."""

    def __init__(
        self,
        jam: BaseJam,
        cookie_name: Optional[str] = "sessionId",
        header_name: Optional[str] = None,
    ) -> None:
        """Constructor.

        Args:
            jam (BaseJam): Jam instance
            cookie_name (str | None): Session id cookie name
            header_name (str | None): Session id header name
        """
        self._jam = jam
        self.cookie_name = cookie_name
        self.header_name = header_name

    async def authenticate(
        self, conn: HTTPConnection
    ) -> Optional[tuple[AuthCredentials, BaseUser]]:
        """Starlette authentication handler."""
        logger = self._jam._BaseJam__logger
        session_id = None

        logger.debug("SessionBackend: Attempting to extract session ID from request")
        if self.cookie_name:
            session_id = conn.cookies.get(self.cookie_name)
            if session_id:
                logger.debug(f"Session ID found in cookie '{self.cookie_name}'")

        if not session_id and self.header_name:
            header = conn.headers.get(self.header_name)
            if header and header.startswith("Bearer "):
                session_id = header.split("Bearer ")[1]
                logger.debug(f"Session ID found in header '{self.header_name}'")

        if not session_id:
            logger.debug("No session ID found in request")
            return None

        logger.debug(f"Getting session data for session ID: {session_id}")
        try:
            payload: dict[str, Any] = await await_maybe(
                self._jam.session_get(session_id)
            )
            if payload:
                logger.debug(f"Session data retrieved successfully, keys: {list(payload.keys())}")
            else:
                logger.debug(f"Session {session_id} not found")
        except Exception as e:
            logger.warning(f"Session retrieval error: {e}")
            raise AuthenticationError("Token verification failed.")

        return AuthCredentials(["authenticated"]), Payload(payload=payload)
