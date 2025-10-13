# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Union


@dataclass
class ProviderNotConfigurError(Exception):
    """Exception if provider not setup."""

    message: Union[str, Exception] = "Provider not setup!"
