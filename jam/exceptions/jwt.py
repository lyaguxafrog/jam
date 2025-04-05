# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class EmptySecretKey(Exception):
    message: str | Exception = "Secret key cannot be NoneType"


@dataclass
class EmtpyPrivateKey(Exception):
    message: str | Exception = "Private key cannot be NoneType"


@dataclass
class EmptyPublicKey(Exception):
    message: str | Exception = "Public key cannot be NoneType"


@dataclass
class TokenLifeTimeExpired(Exception):
    message: str | Exception = "Token lifetime has expired."


class NotFoundSomeInPayload(Exception):
    def __inti__(self, message: str | Exception) -> None:
        self.message: str | Exception = message


@dataclass
class TokenNotInWhiteList(Exception):
    message: str | Exception = "Token not found on white list."


@dataclass
class TokenInBlackList(Exception):
    message: str | Exception = "The token is blacklisted."
