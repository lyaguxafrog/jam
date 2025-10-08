# -*- coding: utf-8 -*-

from typing import Any, Optional, Union

from litestar.config.app import AppConfig
from litestar.di import Provide
from litestar.plugins import InitPlugin

from jam.__abc_instances__ import BaseJam

from .value import AuthMiddlewareSettings, Token, User


class JamPlugin(InitPlugin):
    """Simple Jam plugin for litestar.

    The plugin adds Jam to Litestar DI.

    Example:
        ```python
        from litestar import Litestar
        from jam.ext.litestar import SimpleJamPlugin

        app = Litestar(
            plugins=[SimpleJamPlugin(config="jam_config.toml")],
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
        header_name: Optional[str] = None,
        user_dataclass: Any = User,
        auth_dataclass: Any = Token,
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
        if aio:
            from jam.aio import Jam

            self._instance = Jam(config, pointer)
        else:
            from icecream import ic

            from jam import Jam

            ic(config)
            self._instance = Jam(config=config, pointer=pointer)

        self._settings = AuthMiddlewareSettings(
            cookie_name, header_name, user_dataclass, auth_dataclass
        )

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        """Init app config."""
        from jam.ext.litestar.middlewares import JamJWTMiddleware

        if self._instance.module.list:
            app_config.state.use_list = True
        else:
            app_config.state.use_list = False
        middleware_settings = self._settings
        app_config.state.middleware_settings = middleware_settings
        app_config.state.jam_instance = self._instance
        app_config.middleware = [JamJWTMiddleware]
        return app_config
