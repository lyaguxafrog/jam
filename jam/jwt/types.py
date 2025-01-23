# -*- coding: utf-8 -*-

from typing import Dict


class tokens:
    """Output token type"""

    def __init__(self, access_token: str, refresh_token: str | None) -> None:
        self.access: str = access_token
        self.refresh: str | None = refresh_token

    def to_dict(self) -> Dict[str, str | None]:
        """
        Serializer tokens type to dict

        Example:
        ```python

        token_dict: dict = tokens.to_dict()
        print(tokens)
        # {'access': '<access_token>', 'refresh': '<refresh_token>'}
        ```

        Returns:
            (Dict[str, str | None]): Dict with access and refresh tokens
        """

        return {"access": self.access, "refresh": self.refresh}
