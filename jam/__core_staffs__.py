# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Dict, Literal

from jam.jwt.__tools__ import __gen_jwt__


class AbstractConfig(ABC):
    @abstractmethod
    def __init__(
        self,
        JWT_SECRET_KEY: str | None,
        JWT_PRIVATE_KEY: str | None,
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
        self.JWT_SECRET_KEY: str | None = JWT_SECRET_KEY
        self.JWT_PRIVATE_KEY: str | None = JWT_PRIVATE_KEY
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
    def gen_jwt_tokens(self, **kwargs) -> Dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    def gen_token(self, **kwargs) -> str:
        raise NotImplementedError


class Config(AbstractConfig):
    """
    Base config class
    """

    def __init__(
        self,
        JWT_SECRET_KEY,
        JWT_PRIVATE_KEY,
        JWT_ALGORITHM=None,
        JWT_ACCESS_EXP=3600,
        JWT_REFRESH_EXP=3600,
        JWT_HEADERS=None,
    ):
        super().__init__(
            JWT_SECRET_KEY,
            JWT_ALGORITHM,
            JWT_PRIVATE_KEY,
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

    def gen_token(self, *args):

        header = {"alg": self.config.JWT_ALGORITHM, "type": "jwt"}

        token: str = __gen_jwt__(
            header=header,
            payload=args,
            secret=self.config.JWT_SECRET_KEY,
            private_key=self.config.JWT_PRIVATE_KEY,
        )

        return token
