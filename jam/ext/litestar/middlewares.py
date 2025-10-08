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
            connection.app.state.middleware_settings
        )
        # TODO: Exec jam.modules.JWTModule, not main instance
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
                    instance.verify_jwt_token(
                        token=cookie,
                        check_exp=False,
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
                    instance.verify_jwt_token(
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
