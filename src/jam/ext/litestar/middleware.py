# -*- coding: utf-8 -*-

from collections.abc import Callable

from litestar.connection import ASGIConnection
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)

from jam.aio.sessions.__base__ import BaseAsyncSessionModule
from jam.exceptions import JamLitestarPluginConfigError, JamLitestarPluginError
from jam.ext.litestar.objects import BaseUser, Token
from jam.jose.__base__ import BaseJWT as JWTClass
from jam.paseto import BasePASETO


class BaseMiddleware(AbstractAuthenticationMiddleware):
    """Base Jam middleware for litestar."""

    AUTH_MODULE: Callable
    HEADER_NAME: str | None
    COOKIE_NAME: str | None
    BEARER: bool = False
    USER: type[BaseUser]

    def _get_auth_token(self, connection: ASGIConnection) -> str | None:
        if self.HEADER_NAME:
            token = connection.headers.get(self.HEADER_NAME, None)
            if self.BEARER and token:
                token = token.split(" ")[1]
            return token
        elif self.COOKIE_NAME:
            token = connection.cookies.get(self.COOKIE_NAME, None)
        else:
            raise JamLitestarPluginConfigError(
                message="No header or cookie name provided for JWT authentication.",
                details={
                    "header_name": self.HEADER_NAME,
                    "cookie_name": self.COOKIE_NAME,
                },
            )
        return token


class JWTMiddleware(BaseMiddleware):
    """JWT Middleware for litestar."""

    AUTH_MODULE: JWTClass
    LIST: bool = False

    async def authenticate_request(  # noqa
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        token = self._get_auth_token(connection)
        token_model = Token(token=token)
        if not token:
            return AuthenticationResult(user=None, auth=token_model)
        try:
            result = self.AUTH_MODULE.decode(token)
            data = result.get("payload", result)
            if self.AUTH_MODULE.list and self.LIST:
                match self.AUTH_MODULE.list.__list_type__:
                    case "white":
                        if not self.AUTH_MODULE.list.check(token):
                            return AuthenticationResult(
                                user=None, auth=token_model
                            )
                    case "black":
                        if self.AUTH_MODULE.list.check(token):
                            return AuthenticationResult(
                                user=None, auth=token_model
                            )
            user = self.USER.from_payload(data)

            return AuthenticationResult(user=user, auth=token_model)
        except Exception as e:
            raise JamLitestarPluginError(message=str(e))


class SessionMiddleware(BaseMiddleware):
    """Session middleware for litestar."""

    AUTH_MODULE: BaseAsyncSessionModule

    async def authenticate_request(  # noqa
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        token = self._get_auth_token(connection)
        token_model = Token(token=token)
        if not token:
            return AuthenticationResult(None, auth=token_model)
        try:
            data = await self.AUTH_MODULE.get(token)
            if not data:
                return AuthenticationResult(None, auth=token_model)
            user = self.USER.from_payload(data)
            return AuthenticationResult(user, token)
        except Exception as e:
            raise JamLitestarPluginError(message=str(e))


class PASETOMiddleware(BaseMiddleware):
    """Middleware for PASETO."""

    AUTH_MODULE: BasePASETO

    async def authenticate_request(  # noqa
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        token = self._get_auth_token(connection)
        token_model = Token(token=token)
        if not token:
            return AuthenticationResult(None, auth=token_model)
        try:
            data = self.AUTH_MODULE.decode(token)
            if not data:
                return AuthenticationResult(None, auth=token_model)
            user = self.USER.from_payload(data)
            return AuthenticationResult(user, token)
        except Exception as e:
            raise JamLitestarPluginError(message=str(e))
