# -*- coding: utf-8 -*-

from typing import Any, Optional

from litestar.config.app import AppConfig
from litestar.di import Provide
from litestar.plugins import InitPlugin

from jam.__abc_instances__ import BaseJam

from .value import Auth, AuthMiddlewareSettings, User


class JamPlugin(InitPlugin):
    """Simple Jam plugin for litestar.

    The plugin adds Jam to Litestar DI.

    Example:
        >>> from litestar import Litestar
        >>> from jam import Jam
        >>> from jam.ext.litestar import JamPlugin
        >>> jam = Jam()
        >>> app = Litestar(
        >>>    plugins=[JamPlugin(jam=jam)],
        >>>    router_handlers=[your_router]
        >>>)
    """

    def __init__(
        self,
        jam: BaseJam,
        dependency_key: str = "jam",
    ) -> None:
        """Constructor.

        Args:
            jam (BaseJam): Jam instance
            dependency_key (str): Key in Litestar DI
        """
        self._jam = jam
        self.dependency_key = dependency_key

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        """Litestar init."""
        dependencies = app_config.dependencies or {}
        dependencies[self.dependency_key] = Provide(lambda: self._jam)
        app_config.dependencies = dependencies
        return app_config


class JWTPlugin(InitPlugin):
    """JWT Plugin for litestar."""

    def __init__(
        self,
        jam: BaseJam,
        cookie_name: Optional[str] = None,
        header_name: Optional[str] = "Authorization",
        user_dataclass: Any = User,
        auth_dataclass: Any = Auth,
    ) -> None:
        """Constructor.

        Args:
            jam (BaseJam): Jam instance
            cookie_name (str): Cookie name for token check
            header_name (str): Header name for token check
            user_dataclass (Any): Specific user dataclass
            auth_dataclass (Any): Specific auth dataclass
        """
        self._jam = jam
        self._settings = AuthMiddlewareSettings(
            cookie_name, header_name, user_dataclass, auth_dataclass
        )
        self.__use_list = getattr(self._jam.module, "list", False)

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        """Init app config."""
        from jam.ext.litestar.middlewares import JamJWTMiddleware

        app_config.state.jwt_middleware_settings = self._settings
        app_config.state.jam_instance = self._jam
        app_config.state.use_list = self.__use_list
        app_config.middleware.append(JamJWTMiddleware)
        return app_config


class SessionsPlugin(InitPlugin):
    """Server side sessions plugin for litestar."""

    def __init__(
        self,
        jam: BaseJam,
        cookie_name: Optional[str] = None,
        header_name: Optional[str] = "Authorization",
        user_dataclass: Any = User,
        auth_dataclass: Any = Auth,
    ) -> None:
        """Constructor.

        Args:
            jam (BaseJam): Jam instance
            cookie_name (str): Cookie name for token check
            header_name (str): Header name for token check
            user_dataclass (Any): Specific user dataclass
            auth_dataclass (Any): Specific auth dataclass
        """
        self._jam = jam
        self._settings = AuthMiddlewareSettings(
            cookie_name, header_name, user_dataclass, auth_dataclass
        )

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        """Init application."""
        from jam.ext.litestar.middlewares import JamSessionsMiddleware

        app_config.middleware.append(JamSessionsMiddleware)
        app_config.state.session_middleware_settings = self._settings
        app_config.state.session_instance = self._jam
        return app_config
