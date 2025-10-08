# -*- coding: utf-8 -*-

from typing import Any, Union

from litestar.config.app import AppConfig
from litestar.di import Provide
from litestar.plugins import InitPlugin

from jam.__abc_instances__ import BaseJam


class SimpleJamPlugin(InitPlugin):
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
