# -*- coding: utf-8 -*-

from collections.abc import Callable
from typing import Any

from starlette.authentication import AuthenticationBackend, BaseUser

from jam.exceptions import JamStarlettePluginConfigError
from jam.utils.config_maker import GENERIC_POINTER, __config_maker__


class BaseBackend(AuthenticationBackend):
    """Base Jam backend."""

    MODULE: Callable
    _CONFIG_KEY: str

    def __init__(  # noqa
        self,
        config: str | dict[str, Any] | None = None,
        pointer: str = GENERIC_POINTER,
        cookie_name: str | None = None,
        header_name: str | None = None,
        user: type[BaseUser] | None = None,
        **kwargs,
    ) -> None:
        if not cookie_name and not header_name:
            raise JamStarlettePluginConfigError(
                message="cookie_name or header_name must be provided.",
                details={
                    "cookie_name": cookie_name,
                    "header_name": header_name,
                },
            )
        self._cookie_name = cookie_name
        self._header_name = header_name
        self._user = user
        self._config_setup(config, pointer, kwargs)

    def _config_setup(
        self,
        config: dict[str, Any] | str | None,
        pointer: str,
        kwargs: dict[str, Any],
    ) -> None:
        try:
            if config:
                config_ = __config_maker__(config, pointer)[self._CONFIG_KEY]
                self._auth = self.MODULE(**config_)
            else:
                self._auth = self.MODULE(**kwargs)
        except Exception as e:
            raise JamStarlettePluginConfigError(
                message="Error while building auth modile.",
                details={
                    "module": self.MODULE.__str__,
                    "config": {
                        "config": config,
                        "pointer": pointer,
                        "kwargs": kwargs,
                    },
                    "config_key": self._CONFIG_KEY,
                    "error": str(e),
                },
            )
