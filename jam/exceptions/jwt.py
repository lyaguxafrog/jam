# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Union


@dataclass
class EmptySecretKey(Exception):
    message: Union[str, Exception] = "Secret key cannot be NoneType"


@dataclass
class EmtpyPrivateKey(Exception):
    message: Union[str, Exception] = "Private key cannot be NoneType"


@dataclass
class EmptyPublicKey(Exception):
    message: Union[str, Exception] = "Public key cannot be NoneType"


@dataclass
class TokenLifeTimeExpired(Exception):
    message: Union[str, Exception] = "Token lifetime has expired."


class NotFoundSomeInPayload(Exception):
    def __init__(self, message: Union[str, Exception]) -> None:
        self.message: Union[str, Exception] = message


@dataclass
class TokenNotInWhiteList(Exception):
    message: Union[str, Exception] = "Token not found on white list."


@dataclass
class TokenInBlackList(Exception):
    message: Union[str, Exception] = "The token is blacklisted."
