# -*- coding: utf -*-

from typing import Literal


class JAMConfig:
    """Base config class"""

    def __init__(
        self,
        JWT_ACCESS_SECRET_KEY: str | None,
        JWT_REFRESH_SECRET_KEY: str | None,
        JWT_ALGORITHM: Literal[
            "HS256",
            "HS384",
            "HS512",
            "RS256",
            "RS384",
            "RS512",
            "ES256",
            "ES384",
            "ES512",
            "PS256",
            "PS384",
            "PS512",
        ] = "HS256",
        JWT_ACCESS_EXP: int = 3600,
        JWT_REFRESH_EXP: int = 3600,
        JWT_HEADERS: dict | None = None,
    ):
        self.JWT_ACCESS_SECRET_KEY: str | None = JWT_ACCESS_SECRET_KEY
        self.JWT_REFRESH_SECRET_KEY: str | None = JWT_REFRESH_SECRET_KEY

        self.JWT_ALGORITHM: str = JWT_ALGORITHM

        self.JWT_ACCESS_EXP: int = JWT_ACCESS_EXP
        self.JWT_REFRESH_EXP: int = JWT_REFRESH_EXP

        if not JWT_HEADERS:
            self.JWT_HEADERS: dict = {}
        else:
            self.JWT_HEADERS: dict = JWT_HEADERS
