# -*- coding: utf-8 -*-

"""
Starlette integration.

Starlette docs: https://starlette.dev
"""

from .auth_backends import JWTBackend, SessionBackend


__all__ = ["JWTBackend", "SessionBackend"]
