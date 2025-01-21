# -*- coding: utf-8 -*-


class JamNullJWTSecret(Exception):
    def __init__(self, message="Secret keys cannot be Null") -> None:
        self.message = message


class JamJWTMakingError(Exception):
    def __init__(self, message) -> None:
        self.message = message


class JamInvalidSignature(Exception):
    def __init__(self, message="Invalid signature") -> None:
        self.message = message
