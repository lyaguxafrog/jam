# -*- coding: utf-8 -*-

from collections.abc import Callable
from typing import Any

from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    UnauthenticatedUser,
)
from starlette.authentication import BaseUser as StarletteBaseUser
from starlette.requests import HTTPConnection

from jam.aio.sessions import create_instance as create_session
from jam.exceptions import JamStarlettePluginConfigError
from jam.ext.starlette.objects import BaseUser, SimpleUser
from jam.jwt import create_instance as create_jwt
from jam.paseto import create_instance as create_paseto
from jam.utils.config_maker import GENERIC_POINTER, __config_maker__


class BaseBackend(AuthenticationBackend):
    """Base Jam backend."""

    MODULE: Callable
    _CONFIG_KEY: str

    def __init__(  # noqa
        self,
        config: str | dict[str, Any] | None = None,
        pointer: str = GENERIC_POINTER,
        cookie_name: str | None = None,
        header_name: str | None = None,
        bearer: bool = False,
        user: type[BaseUser] = SimpleUser,
        **kwargs,
    ) -> None:
        if not cookie_name and not header_name:
            raise JamStarlettePluginConfigError(
                message="cookie_name or header_name must be provided.",
                details={
                    "cookie_name": cookie_name,
                    "header_name": header_name,
                },
            )
        self._cookie_name = cookie_name
        self._header_name = header_name
        self._bearer = bearer
        self._user = user
        self._config_setup(config, pointer, kwargs)

    def _get_auth_token(self, connection: HTTPConnection) -> str | None:
        if self._cookie_name:
            token = connection.cookies.get(self._cookie_name, None)
        elif self._header_name:
            token_bear = connection.headers.get(self._header_name, None)
            if token_bear:
                token = (
                    token_bear.split("Bearer ")[1]
                    if self._bearer
                    else token_bear
                )  # noqa: E701
            else:
                token = None  # noqa: E701
        else:
            raise JamStarlettePluginConfigError(
                message="cookie_name or header_name must be provided.",
                details={
                    "cookie_name": self._cookie_name,
                    "header_name": self._header_name,
                },
            )
        return token

    def _config_setup(
        self,
        config: dict[str, Any] | str | None,
        pointer: str,
        kwargs: dict[str, Any],
    ) -> None:
        try:
            if config:
                config_ = __config_maker__(config, pointer)[self._CONFIG_KEY]
                self._auth = self.MODULE(**config_)
            else:
                self._auth = self.MODULE(**kwargs)
        except Exception as e:
            raise JamStarlettePluginConfigError(
                message="Error while building auth modile.",
                details={
                    "module": self.MODULE.__str__,
                    "config": {
                        "config": config,
                        "pointer": pointer,
                        "kwargs": kwargs,
                    },
                    "config_key": self._CONFIG_KEY,
                    "error": str(e),
                },
            )


class JWTBackend(BaseBackend):
    """JWT Backend for litestar."""

    MODULE = staticmethod(create_jwt)
    _CONFIG_KEY = "jwt"

    def __init__(  # noqa
        self,
        config: str | dict[str, Any] | None = None,
        pointer: str = GENERIC_POINTER,
        cookie_name: str | None = None,
        header_name: str | None = None,
        use_list: bool = False,
        user: type[BaseUser] = SimpleUser,
        **kwargs,
    ) -> None:
        self.use_list = use_list
        super().__init__(
            config=config,
            pointer=pointer,
            cookie_name=cookie_name,
            header_name=header_name,
            user=user,
            **kwargs,
        )

    async def authenticate(  # noqa
        self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, StarletteBaseUser] | None:
        setattr(conn.state, "jwt", self._auth)
        token = self._get_auth_token(conn)
        if token:
            if self.use_list:
                match self._auth.list.__list_type__:
                    case "black":
                        if self._auth.list.check(token):
                            return AuthCredentials(None), UnauthenticatedUser()
                    case "white":
                        if self._auth.list.check(token):
                            return AuthCredentials(None), UnauthenticatedUser()
            data = self._auth.decode(token)
            user = self._user.from_payload(data)
            return AuthCredentials(["authenticated"]), user

        return AuthCredentials(None), UnauthenticatedUser()


class SessionBackend(BaseBackend):
    """Session backend."""

    MODULE = staticmethod(create_session)
    _CONFIG_KEY = "sessions"

    async def authenticate(  # noqa
        self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, StarletteBaseUser] | None:
        setattr(conn.state, "session", self._auth)
        session_id = self._get_auth_token(conn)
        if session_id:
            data = await self._auth.get(session_id)
            if data:
                user = self._user.from_payload(data)
                return AuthCredentials(["authenticated"]), user

        return AuthCredentials(None), UnauthenticatedUser()


class PASETOBackend(BaseBackend):
    """PASETO auth backend."""

    MODULE = staticmethod(create_paseto)
    _CONFIG_KEY = "paseto"

    async def authenticate(  # noqa
        self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, StarletteBaseUser] | None:
        setattr(conn.state, "paseto", self._auth)
        token = self._get_auth_token(conn)
        if token:
            data = self._auth.decode(token)
            if data:
                user = self._user.from_payload(data)
                return AuthCredentials(["authenticated"]), user

        return AuthCredentials(None), UnauthenticatedUser()
