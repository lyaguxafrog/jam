# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class ProviderNotConfigurError(Exception):
    """Exception if provider not setup."""

    message: str = "Provider not setup!"
