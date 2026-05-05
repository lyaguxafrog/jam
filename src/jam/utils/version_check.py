# -*- coding: utf-8 -*-

from importlib.metadata import version

from packaging.version import Version


def __is_compatible__(
    income_version: str | None, required_version: str
) -> bool:
    """Checks if the income version is compatible with the required version."""
    current = Version(income_version or version("jamlib"))
    required = Version(required_version)

    if current.major != required.major:
        return False

    return current >= required
