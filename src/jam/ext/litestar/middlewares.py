# -*- coding: utf-8 -*-

from litestar.connection import ASGIConnection
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)

from jam.__abc_instances__ import BaseJam
from jam.utils.await_maybe import await_maybe


class JamJWTMiddleware(AbstractAuthenticationMiddleware):
    """JWT Middleware."""

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        """Auth request."""
        from jam.ext.litestar.value import AuthMiddlewareSettings

        settings: AuthMiddlewareSettings = (
            connection.app.state.jwt_middleware_settings
        )
        instance: BaseJam = connection.app.state.jam_instance

        cookie = (
            connection.cookies.get(settings.cookie_name, None)
            if settings.cookie_name
            else None
        )
        header = (
            connection.headers.get(settings.header_name, None)
            if settings.header_name
            else None
        )
        if cookie:
            try:
                payload = await await_maybe(
                    instance.jwt_verify_token(
                        token=cookie,
                        check_exp=True,  # NOTE: Expire always check
                        check_list=connection.app.state.use_list,
                    )
                )

                # FIXME: Generic classes
                token = settings.auth_dataclass(token=cookie)
                user = settings.user_dataclass(payload=payload)
                return AuthenticationResult(user, token)

            except Exception:
                pass
        if header:
            try:
                payload = await await_maybe(
                    instance.jwt_verify_token(
                        token=cookie,
                        check_exp=True,
                        check_list=connection.app.state.use_list,
                    )
                )

                # FIXME: Generic classes
                token = settings.auth_dataclass(token=header)
                user = settings.user_dataclass(payload=payload)
                return AuthenticationResult(user, token)

            except Exception:
                pass

        return AuthenticationResult(None, None)


class JamSessionsMiddleware(AbstractAuthenticationMiddleware):
    """Jam sessions middleware for litestar."""

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        """Auth request."""
        from jam.ext.litestar.value import AuthMiddlewareSettings

        settings: AuthMiddlewareSettings = (
            connection.app.state.session_middleware_settings
        )
        instance: BaseJam = connection.app.state.session_instance

        cookie = (
            connection.cookies.get(settings.cookie_name, None)
            if settings.cookie_name
            else None
        )
        header = (
            connection.headers.get(settings.header_name, None)
            if settings.header_name
            else None
        )

        if cookie:
            payload = await await_maybe(instance.session_get(cookie))
            return AuthenticationResult(
                settings.user_dataclass(payload=payload),
                settings.auth_dataclass(token=cookie),
            )
        if header:
            payload = await await_maybe(instance.session_get(header))
            return AuthenticationResult(
                settings.user_dataclass(payload=payload),
                settings.auth_dataclass(token=header),
            )

        return AuthenticationResult(None, None)
