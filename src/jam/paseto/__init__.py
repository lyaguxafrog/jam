# -*- coding: utf-8 -*-

"""PASETO auth* tokens."""

import os
from typing import Any, Literal, Union

from .__abc_paseto_repo__ import PASETO, BasePASETO
from .v1 import PASETOv1
from .v2 import PASETOv2
from .v3 import PASETOv3
from .v4 import PASETOv4
from jam.logger import BaseLogger, logger


def create_instance(
    version: Literal["v1", "v2", "v3", "v4"],
    purpose: Literal["local", "public"],
    key: Union[str, bytes, Any],
    logger: BaseLogger = logger,
    **kwargs: Any
) -> PASETO:
    """Create PASETO instance.

    Args:
        version (str): "v1" | "v2" | "v3" | "v4"
        purpose (str): "local" | "public"
        key (str | bytes | Any): Secret or asymmetric key (can be file path)
        logger (BaseLogger): Logger instance
        **kwargs: Additional params (e.g., custom_module)

    Returns:
        PASETO instance
    """
    from jam.utils.config_maker import __module_loader__

    if isinstance(key, str) and os.path.isfile(key):
        with open(key) as f:
            key = f.read()

    if kwargs.get("custom_module"):
        module_cls = __module_loader__(kwargs["custom_module"])
        return module_cls.key(purpose, key)

    module_cls = __module_loader__(f"jam.paseto.{version}.PASETO{version}")
    return module_cls.key(purpose, key)


__all__ = [
    "PASETO",
    "BasePASETO",
    "PASETOv1",
    "PASETOv2",
    "PASETOv3",
    "PASETOv4",
    "create_instance",
]
