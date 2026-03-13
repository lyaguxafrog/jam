# -*- coding: utf-8 -*-

"""Flask integration.

Flask docs: https://flask.palletsprojects.com
"""

from .extensions import (
    JWTExtension,
    OAuth2Extension,
    PASETOExtension,
    SessionExtension,
)

from .objects import (
    BaseUser,
    SimpleUser,
    Token,
)


__all__ = [
    "BaseUser",
    "SimpleUser",
    "Token",
    "JWTExtension",
    "SessionExtension",
    "PASETOExtension",
    "OAuth2Extension",
]
