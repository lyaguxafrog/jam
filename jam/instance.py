# -*- coding: utf-8 -*-

from jam.config import JAMConfig
from jam.jwt.tools import gen_jwt_tokens
from jam.jwt.types import tokens


class Jam:
    """Base Jam class"""

    config: JAMConfig

    def __init__(self, config: JAMConfig) -> None:
        self.config: JAMConfig = config

    def jwt_gen_tokens(self, payload: dict | None = None) -> tokens:
        """
        Service for generating access and refresh tokend by config

        :param payload: Payload for stacking in token
        :type payload: dict

        :returns: Tokens
        :rtype: jam.jwt.types.tokens
        """

        jwt_tokens: tokens = gen_jwt_tokens(config=self.config, payload=payload)
        return jwt_tokens
