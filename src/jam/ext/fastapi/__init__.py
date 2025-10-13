# -*- coding: utf-8 -*-

"""FastAPI integration.

FastAPI docs: https://fastapi.tiangolo.com/
"""

from jam.ext.starlette import JWTBackend, SessionBackend


__all__ = ["JWTBackend", "SessionBackend"]
