# -*- coding: utf-8 -*-


class tokens:
    """Output token type"""

    def __init__(self, access_token: str, refresh_token: str | None) -> None:
        self.access: str = access_token
        self.refresh: str | None = refresh_token
