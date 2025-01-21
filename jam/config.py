# -*- coding: utf -*-

from typing import Literal

from pydantic_settings import BaseSettings


class JAMConfig(BaseSettings):
    JWT_ACCESS_SECRET_KEY: str | None
    JWT_REFRESH_SECRET_KEY: str | None
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
    ] = "HS256"

    JWT_ACCESS_EXP: int = 3600
    JWT_REFRESH_EXP: int = JWT_ACCESS_EXP
    JWT_HEADERS: dict = {}
