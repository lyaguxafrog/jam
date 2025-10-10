# -*- coding: utf-8 -*-

from typing import Any, Optional, Union

from litestar.config.app import AppConfig
from litestar.di import Provide
from litestar.plugins import InitPlugin

from jam.__abc_instances__ import BaseJam
from jam.utils.config_maker import __config_maker__

from .value import Auth, AuthMiddlewareSettings, User


class JamPlugin(InitPlugin):
    """Simple Jam plugin for litestar.

    The plugin adds Jam to Litestar DI.

    Example:
        ```python
        from litestar import Litestar
        from jam.ext.litestar import JamPlugin

        app = Litestar(
            plugins=[JamPlugin(config="jam_config.toml")],
            router_handlers=[your_router]
        )
        ```
    """

    def __init__(
        self,
        config: Union[str, dict[str, Any]] = "pyproject.toml",
        pointer: str = "jam",
        dependency_key: str = "jam",
        aio: bool = False,
    ) -> None:
        """Constructor.

        Args:
            config (str | dict[str, Any]): Jam config
            pointer (str): Config pointer
            dependency_key (str): Key in Litestar DI
            aio (bool): Use jam.aio?
        """
        self.instance: BaseJam
        self.dependency_key = dependency_key
        if aio:
            from jam.aio import Jam

            self.instance = Jam(config, pointer)
        else:
            from jam import Jam

            self.instance = Jam(config, pointer)

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        """Litestar init."""
        dependencies = app_config.dependencies or {}
        dependencies[self.dependency_key] = Provide(lambda: self.instance)
        app_config.dependencies = dependencies
        return app_config


class JWTPlugin(InitPlugin):
    """JWT Plugin for litestar."""

    def __init__(
        self,
        config: Union[str, dict[str, Any]] = "pyproject.toml",
        pointer: str = "jam",
        aio: bool = False,
        cookie_name: Optional[str] = None,
        header_name: Optional[str] = "Authorization",
        user_dataclass: Any = User,
        auth_dataclass: Any = Auth,
    ) -> None:
        """Constructor.

        Args:
            config (str | dict[str, Any]): Jam config
            pointer (str): Config pointer
            aio (bool): Use async jam?
            cookie_name (str): Cookie name for token check
            header_name (str): Header name for token check
            user_dataclass (Any): Specific user dataclass
            auth_dataclass (Any): Specific auth dataclass
        """
        cfg = __config_maker__(config, pointer).copy()
        cfg.pop("auth_type")
        if aio:
            from jam.modules import JWTModule

            self._instance = JWTModule(**cfg)
        else:
            from jam.modules import JWTModule

            self._instance = JWTModule(**cfg)

        self._settings = AuthMiddlewareSettings(
            cookie_name, header_name, user_dataclass, auth_dataclass
        )

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        """Init app config."""
        from jam.ext.litestar.middlewares import JamJWTMiddleware

        if self._instance.list:
            app_config.state.use_list = True
        else:
            app_config.state.use_list = False
        app_config.state.jwt_middleware_settings = self._settings
        app_config.state.jam_instance = self._instance
        app_config.middleware.append(JamJWTMiddleware)
        return app_config


class SessionsPlugin(InitPlugin):
    """Server side sessions plugin for litestar."""

    def __init__(
        self,
        config: Union[str, dict[str, Any]] = "pyproject.toml",
        pointer: str = "jam",
        aio: bool = False,
        cookie_name: Optional[str] = None,
        header_name: Optional[str] = "Authorization",
        user_dataclass: Any = User,
        auth_dataclass: Any = Auth,
    ) -> None:
        """Constructor.

        Args:
            config (str | dict[str, Any]): Jam config
            pointer (str): Config pointer
            aio (bool): Use async jam?
            cookie_name (str): Cookie name for token check
            header_name (str): Header name for token check
            user_dataclass (Any): Specific user dataclass
            auth_dataclass (Any): Specific auth dataclass
        """
        cfg = __config_maker__(config, pointer).copy()
        cfg.pop("auth_type")
        if aio:
            from jam.aio.modules import SessionModule

            self._instance = SessionModule(**cfg)
        else:
            from jam.modules import SessionModule

            self._instance = SessionModule(**cfg)

        self._settings = AuthMiddlewareSettings(
            cookie_name, header_name, user_dataclass, auth_dataclass
        )

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        """Init application."""
        from jam.ext.litestar.middlewares import JamSessionsMiddleware

        app_config.middleware.append(JamSessionsMiddleware)
        app_config.state.session_middleware_settings = self._settings
        app_config.state.session_instance = self._instance
        return app_config
