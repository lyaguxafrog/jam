# -*- coding: utf -*-

from typing import Literal

from pydantic_settings import BaseSettings


class JAMConfig(BaseSettings):
    JWT_SECRET_KEY: str
    ALGHORYTM: Literal[
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
        "PS512"
    ] = "HS256"

    HEADERS: dict
