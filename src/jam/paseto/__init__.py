# -*- coding: utf-8 -*-

"""PASETO auth* tokens."""

from .__abc_paseto_repo__ import PASETO, BasePASETO
from .v1 import PASETOv1
from .v2 import PASETOv2
from .v3 import PASETOv3
from .v4 import PASETOv4


__all__ = [
    "PASETO",
    "BasePASETO",
    "PASETOv1",
    "PASETOv2",
    "PASETOv3",
    "PASETOv4",
]
