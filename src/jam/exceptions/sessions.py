# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Union


@dataclass
class SessionNotFoundError(Exception):
    """Exception raised when a session is not found."""

    message: Union[str, Exception] = "Session not found."
