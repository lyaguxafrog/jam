# -*- coding: utf-8 -*-

from collections.abc import Callable
from typing import Any

from litestar.config.app import AppConfig
from litestar.di import Provide
from litestar.plugins import InitPlugin

from jam.exceptions import JamLitestarPluginConfigError
from jam.ext.litestar.objects import BaseUser
from jam.jwt import JWT
from jam.utils.config_maker import GENERIC_POINTER, __config_maker__


class BasePlugin(InitPlugin):
    """Base Litestar plugin."""

    MODULE: Callable

    def _setup_config(self, config: dict[str, Any]) -> None:
        self._auth = self.MODULE(**config)


class JamJWTPlugin(BasePlugin):
    """JWT plugin for litestar."""

    MODULE = JWT

    def __init__(  # noqa
        self,
        config: dict[str, Any] | str | None = None,
        pointer: str = GENERIC_POINTER,
        cookie_name: str | None = None,
        header_name: str | None = None,
        middleware: bool = True,
        middleware_user: type[BaseUser] | None = None,
        **kwargs,
    ) -> None:
        if middleware and (not cookie_name and not header_name):
            raise JamLitestarPluginConfigError(
                message="Cookie name and header name cannot be both None.",
                details={
                    "cookie_name": cookie_name,
                    "header_name": header_name,
                },
            )
        if middleware and not middleware_user:
            raise JamLitestarPluginConfigError(
                message="Middleware user cannot be None when middleware is True.",
                details={
                    "middleware_user": middleware_user,
                },
            )

        _config: dict[str, Any] | None = (
            __config_maker__(config, pointer) if config else None
        )

        self._auth = self.MODULE(**(_config if _config else kwargs))
        self._middleware = None

        if middleware:
            from jam.ext.litestar.middleware import JWTMiddleware

            _middleware = JWTMiddleware
            _middleware.COOKIE_NAME = cookie_name
            _middleware.HEADER_NAME = header_name
            _middleware.AUTH_MODULE = self._auth
            _middleware.USER = middleware_user  # type: ignore
            self._middleware = _middleware

    def on_app_init(self, app_config: AppConfig) -> AppConfig:  # noqa
        app_config.dependencies["jwt"] = Provide(
            lambda: self._auth, sync_to_thread=True
        )
        app_config.middleware.append(
            self._middleware
        ) if self._middleware else None
        return app_config
