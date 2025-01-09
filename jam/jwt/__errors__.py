# -*- coding: utf-8 -*-


class JamNullJWTSecret(Exception):
    def __init__(self, message="Secret keys cannot be Null") -> None:
        self.message = message
