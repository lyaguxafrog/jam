# -*- coding: utf-8 -*-

from typing import Any


class JamError(Exception):
    """Base jam exception.

    Support:
    - message: human-readable message
    - error_code: machine-readable error code
    - details: additional data
    """

    default_message = "An unknown jam error occurred."
    default_code = "jam.error"

    __slots__ = ["error_code", "details"]

    def __init__(
        self,
        message: str | None = None,
        *,
        error_code: str | None = None,
        details: Any | None = None,
    ) -> None:
        message = message or self.default_message
        super().__init__(message)

        self.error_code = error_code or self.default_code
        self.details = details

    @property
    def message(self) -> str:
        """Human-readable message."""
        return self.args[0]

    def __str__(self) -> str:
        base = f"[{self.error_code}] {self.message}"
        if self.details is not None:
            return f"{base} | details={self.details}"
        return base

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"error_code={self.error_code!r}, "
            f"details={self.details!r})"
        )


class JamValidationError(JamError):
    """Exception raised when a validation error occurs."""

    default_message = "Validation error occurred."
    default_code = "jam.validation"


class JamConfigurationError(JamError):
    """Exception raised when a configuration error occurs."""

    default_message = "Configuration error occurred."
    default_code = "jam.configuration"
