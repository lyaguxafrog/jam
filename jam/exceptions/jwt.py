# -*- coding: utf-8 -*-


class EmptySecretKey(Exception):
    def __init__(
        self, message: str | Exception = "Secret key cannot be NoneType"
    ) -> None:
        self.message: str | Exception = message

    def __str__(self) -> str:
        return str(self.message)


class EmtpyPrivateKey(Exception):
    def __init__(
        self, message: str | Exception = "Private key cannot be NoneType"
    ) -> None:
        self.message: str | Exception = message

    def __str__(self) -> str:
        return str(self.message)
