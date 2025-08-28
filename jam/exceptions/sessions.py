# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class SessionNotFoundError(Exception):
    """Exception raised when a session is not found."""

    message: str | Exception = "Session not found."
