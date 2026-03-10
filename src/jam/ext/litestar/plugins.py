# -*- coding: utf-8 -*-

from collections.abc import Callable
from typing import Any

from litestar.config.app import AppConfig
from litestar.di import Provide
from litestar.plugins import InitPlugin

from jam.exceptions import JamLitestarPluginConfigError
from jam.jwt import JWT
from jam.utils.config_maker import GENERIC_POINTER, __config_maker__


class BasePlugin(InitPlugin):
    """Base Litestar plugin."""

    _AUTH_MODULE: Callable

    def _setup_config(self, config: dict[str, Any]) -> None:
        self._auth = self._AUTH_MODULE(**config)


class JamJWTPlugin(BasePlugin):
    """JWT plugin for litestar."""

    _AUTH_MODULE = JWT

    def __init__(  # noqa
        self,
        config: dict[str, Any] | str | None = None,
        pointer: str = GENERIC_POINTER,
        cookie_name: str | None = None,
        header_name: str | None = None,
        **kwargs,
    ) -> None:
        if not cookie_name and not header_name:
            raise JamLitestarPluginConfigError(
                message="Cookie name and header name cannot be both None.",
                details={
                    "cookie_name": cookie_name,
                    "header_name": header_name,
                },
            )

        _config: dict[str, Any] | None = (
            (__config_maker__(config, pointer)) if config else None
        )

    def on_app_init(self, app_config: AppConfig) -> AppConfig:  # noqa: D102
        app_config.dependencies["jwt"] = Provide(
            lambda: self._auth, sync_to_thread=True
        )
        return app_config
