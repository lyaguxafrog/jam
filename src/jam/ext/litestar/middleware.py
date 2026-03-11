# -*- coding: utf-8 -*-

from litestar.connection import ASGIConnection
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)

from jam.exceptions import JamLitestarPluginConfigError, JamLitestarPluginError
from jam.ext.litestar.objects import BaseUser, Token
from jam.jwt import JWT


class BaseMiddleware(AbstractAuthenticationMiddleware):
    """Base Jam middleware for litestar."""

    HEADER_NAME: str | None
    COOKIE_NAME: str | None
    AUTH_MODULE: JWT
    USER: type[BaseUser]

    def _get_auth_token(self, connection: ASGIConnection) -> str | None:
        if self.HEADER_NAME:
            token = connection.headers.get(self.HEADER_NAME, None)
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

    async def authenticate_request(  # noqa
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        token = self._get_auth_token(connection)
        token_model = Token(token=token)
        if not token:
            return AuthenticationResult(None, auth=token_model)
        try:
            data = self.AUTH_MODULE.decode(token)
            user = self.USER.from_payload(data)

            return AuthenticationResult(user, token_model)
        except Exception as e:
            raise JamLitestarPluginError(message=str(e))
