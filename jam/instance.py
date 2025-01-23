# -*- coding: utf-8 -*-

from typing import Literal

from jam.config import JAMConfig
from jam.jwt.tools import decode_token, gen_jwt_tokens
from jam.jwt.types import tokens


class Jam:
    """Base Jam class"""

    config: JAMConfig

    def __init__(self, config: JAMConfig) -> None:
        self.config: JAMConfig = config

    def jwt_gen_tokens(self, payload: dict | None = None) -> tokens:
        """
        Service for generating access and refresh tokend by config

        Args:
            payload (dict | None): Payload with data

        Returns:
            JWT Tokens
        """

        jwt_tokens: tokens = gen_jwt_tokens(config=self.config, payload=payload)
        return jwt_tokens

    def jwt_decode_token(
        self,
        token: str,
        checksum: bool = False,
        token_type: Literal["access", "refresh"] | None = None,
    ) -> dict:
        """
        Method for decode token data

        Args:
            token (str): Your JWT token
            checksum (bool): Make `True` if you need to check signature
            token_type (str): Access or refresh(need while checking sum)

        Returns:
            (dict): Dict with decoded data
        """

        decoded: dict = decode_token(
            config=self.config,
            token=token,
            checksum=checksum,
            checksum_token_type=token_type,
        )
        return decoded
