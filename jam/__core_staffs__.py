# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Literal


class AbstractConfig(ABC):
    @abstractmethod
    def __init__(
        self,
        JWT_ACCESS_SECRET_KEY: str | None,
        JWT_REFRESH_SECRET_KEY: str | None,
        JWT_ALGORITHM: (
            Literal[
                "HS256",
                "HS384",
                "HS512",
                "RS256",
                "RS384",
                "RS512",
                "PS256",
                "PS384",
                "PS512",
            ]
            | None  # noqa
        ) = None,
        JWT_ACCESS_EXP: int = 3600,
        JWT_REFRESH_EXP: int = 3600,
        JWT_HEADERS: dict | None = None,
    ) -> None:
        self.JWT_ACCESS_SECRET_KEY: str | None = JWT_ACCESS_SECRET_KEY
        self.JWT_REFRESH_SECRET_KEY: str | None = JWT_REFRESH_SECRET_KEY

        self.JWT_ALGORITHM: str | None = JWT_ALGORITHM

        self.JWT_ACCESS_EXP: int = JWT_ACCESS_EXP
        self.JWT_REFRESH_EXP: int = JWT_REFRESH_EXP

        if not JWT_HEADERS:
            self.JWT_HEADERS: dict = {}
        else:
            self.JWT_HEADERS: dict = JWT_HEADERS


class AbstractIntance(ABC):
    config: AbstractConfig

    @abstractmethod
    def __init__(self, config: AbstractConfig) -> None:
        self.config = config

    @abstractmethod
    def gen_jwt_tokens(self, **kwargs) -> Any:
        raise NotImplementedError


class Config(AbstractConfig):
    """
    Base config class

    Args:
        JWT_ACCESS_SECRET_KEY (str | None): Access secret key
    """

    def __init__(
        self,
        JWT_ACCESS_SECRET_KEY,
        JWT_REFRESH_SECRET_KEY,
        JWT_ALGORITHM=None,
        JWT_ACCESS_EXP=3600,
        JWT_REFRESH_EXP=3600,
        JWT_HEADERS=None,
    ):
        super().__init__(
            JWT_ACCESS_SECRET_KEY,
            JWT_REFRESH_SECRET_KEY,
            JWT_ALGORITHM,
            JWT_ACCESS_EXP,
            JWT_REFRESH_EXP,
            JWT_HEADERS,
        )


class Jam(AbstractIntance):
    """
    Base Jam instance

    Args:
        config (jam.Config): jam.Config
    """

    def __init__(self, config: Config):
        super().__init__(config)
