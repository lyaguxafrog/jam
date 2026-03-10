# -*- coding: utf-8 -*-

from collections.abc import Callable
from typing import Any

from litestar.plugins import InitPlugin

from jam.utils.config_maker import GENERIC_POINTER, __config_maker__


class BasePlugin(InitPlugin):
    """Base Litestar plugin."""

    __AUTH_MODULE: Callable

    def __init__(
        self,
        config: dict[str, Any] | str | None = None,
        pointer: str = GENERIC_POINTER,
        **kwargs,
    ) -> None:
        """Initialize the plugin.

        Args:
            config (dict[str, Any] | str | None): Jam config.
            pointer (str): Pointer to the config.
            **kwargs: Additional keyword arguments for the auth module.
        """
        _config = __config_maker__(config, pointer) if config else None
        self.__auth = self.__AUTH_MODULE(**(_config if _config else kwargs))
