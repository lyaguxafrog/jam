# -*- coding: utf-8 -*-

# TODO: Exceptions to dataclasses

from dataclasses import dataclass


class EmptySecretKey(Exception):
    def __init__(
        self, message: str | Exception = "Secret key cannot be NoneType"
    ) -> None:
        self.message: str | Exception = message


class EmtpyPrivateKey(Exception):
    def __init__(
        self, message: str | Exception = "Private key cannot be NoneType"
    ) -> None:
        self.message: str | Exception = message


class EmptyPublicKey(Exception):
    def __inti__(
        self, message: str | Exception = "Public key cannot be NoneType"
    ) -> None:
        self.message: str | Exception = message


class TokenLifeTimeExpired(Exception):
    def __inti__(
        self, message: str | Exception = "Token lifetime has expired."
    ) -> None:
        self.message: str | Exception = message


class NotFoundSomeInPayload(Exception):
    def __inti__(self, message: str | Exception) -> None:
        self.message: str | Exception = message


@dataclass
class TokenNotInWhiteList(Exception):
    message: str | Exception = "Token not found on white list."


@dataclass
class TokenInBlackList(Exception):
    message: str | Exception = "The token is blacklisted."
