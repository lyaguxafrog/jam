# -*- coding: utf-8 -*-

from jam.config import JAMConfig


class Jam:
    """Base Jam class"""

    def __init__(self, config: JAMConfig) -> None:
        self.config: JAMConfig = config
