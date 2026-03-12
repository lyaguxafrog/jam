# -*- coding: utf-8 -*-

from collections.abc import Callable
from typing import Any

from litestar.config.app import AppConfig
from litestar.di import Provide
from litestar.plugins import InitPlugin

from jam.aio.sessions import create_instance as create_session
from jam.exceptions import JamLitestarPluginConfigError
from jam.ext.litestar.middleware import (
    BaseMiddleware,
    JWTMiddleware,
    PASETOMiddleware,
    SessionMiddleware,
)
from jam.ext.litestar.objects import BaseUser
from jam.jwt import JWT
from jam.oauth2 import create_instance as create_oauth2
from jam.paseto import create_instance as create_paseto
from jam.utils.config_maker import GENERIC_POINTER, __config_maker__


class BasePlugin(InitPlugin):
    """Base Litestar plugin."""

    MODULE: Callable
    MIDDLEWARE: type[BaseMiddleware]
    _DI_KEY: str
    _CONFIG_KEY: str

    def _setup_config(self, config: dict[str, Any]) -> None:
        self._auth = self.MODULE(**config)

    def __init__(
        self,
        config: dict[str, Any] | str | None = None,
        pointer: str = GENERIC_POINTER,
        cookie_name: str | None = None,
        header_name: str | None = None,
        middleware: bool = True,
        user: type[BaseUser] | None = None,
        **kwargs,
    ) -> None:
        """Initialize the plugin.

        Args:
            config (dict[str, Any] | str | None): Jam config as path/to/file or dict.
            pointer (str): Config pointer
            cookie_name (str | None): Cookie name to read token
            header_name (str | None): Header name to read token
            middleware (bool): Use middleware?
            user (type[BaseUser]): User for request state. See: DOCUMENTATION
            **kwargs: Config arguments if config=None
        """
        if middleware and (not cookie_name and not header_name):
            raise JamLitestarPluginConfigError(
                message="Cookie name and header name cannot be both None.",
                details={
                    "cookie_name": cookie_name,
                    "header_name": header_name,
                },
            )
        if middleware and not user:
            raise JamLitestarPluginConfigError(
                message="Middleware user cannot be None when middleware is True.",
                details={
                    "middleware_user": user,
                },
            )

        _config: dict[str, Any] | None = (
            __config_maker__(config, pointer) if config else None
        )

        params = _config.pop(self._CONFIG_KEY) if _config else kwargs
        self._setup_config(params)
        self._middleware = None

        if middleware:
            _middleware = self.MIDDLEWARE
            _middleware.COOKIE_NAME = cookie_name
            _middleware.HEADER_NAME = header_name
            _middleware.AUTH_MODULE = self._auth
            _middleware.USER = user  # type: ignore
            self._middleware = _middleware

    def on_app_init(self, app_config: AppConfig) -> AppConfig:  # noqa
        app_config.dependencies[self._DI_KEY] = Provide(
            lambda: self._auth, sync_to_thread=True
        )
        app_config.middleware.append(
            self._middleware
        ) if self._middleware else None
        return app_config


class JamJWTPlugin(BasePlugin):
    """JWT plugin for litestar."""

    MODULE = JWT
    MIDDLEWARE = JWTMiddleware
    _DI_KEY = "jwt"
    _CONFIG_KEY = "jwt"


class JamSessionPlugin(BasePlugin):
    """Sessions plugin for litestar."""

    MODULE = staticmethod(create_session)
    MIDDLEWARE = SessionMiddleware
    _DI_KEY = "session"
    _CONFIG_KEY = "sessions"


class JamPASETOPlugin(BasePlugin):
    """PASETO plugin for litestar."""

    MODULE = staticmethod(create_paseto)
    MIDDLEWARE = PASETOMiddleware
    _DI_KEY = "paseto"
    _CONFIG_KEY = "paseto"


class JamOAuth2Plugin(BasePlugin):
    """OAuth2 plugin for litestar."""

    MODULE = staticmethod(create_oauth2)
    _DI_KEY = "oauth2"
    _CONFIG_KEY = "oauth2"

    def __init__(
        self,
        config: str | dict[str, Any] | None = None,
        pointer: str = GENERIC_POINTER,
        **kwargs,
    ) -> None:
        """Initialize the OAuth2 plugin.

        Args:
            config (dict[str, Any] | str | None): Jam config as path/to/file or dict.
            pointer (str): Config pointer
            **kwargs: Config arguments if config=None
        """
        _config: dict[str, Any] | None = (
            __config_maker__(config, pointer) if config else None
        )

        params = _config.pop(self._CONFIG_KEY) if _config else kwargs
        self._setup_config(params)

    def on_app_init(self, app_config: AppConfig) -> AppConfig:  # noqa
        app_config.dependencies[self._DI_KEY] = Provide(
            lambda: self._auth, sync_to_thread=True
        )
        return app_config
