# -*- coding: utf-8 -*-

# TODO: Exceptions to dataclasses


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
