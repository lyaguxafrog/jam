# -*- coding: utf-8 -*-

import time
from typing import Literal

from jam.otp.__abc_module__ import BaseOTP


class TOTP(BaseOTP):
    """TOTP (Time-based One-Time Password, RFC6238)."""

    def __init__(
        self,
        secret: bytes | str,
        digits: int = 6,
        digest: Literal["sha1", "sha256", "sha512"] = "sha1",
        interval: int = 30,
    ) -> None:
        """TOTP initialization.

        Args:
            secret (bytes | str): Secret key.
            digits (int, optional): Number of digits in the code. Default is 6.
            digest (str, optional): Hashing algorithm. Default is "sha1".
            interval (int, optional): Time interval in seconds. Default is 30.
        """
        super().__init__(secret, digits, digest)
        self.interval = interval

    def at(self, factor: int | None = None) -> str:
        """Generates a TOTP code for a specified time.

        Args:
            factor (int | None, optional): Time in UNIX seconds. If None, the current time is used. Default is None.

        Returns:
            str: TOTP code (fixed-length string).
        """
        if factor is None:
            factor = int(time.time())
        counter = factor // self.interval
        return str(self._dynamic_truncate(self._hmac(counter))).zfill(
            self.digits
        )

    @property
    def now(self) -> str:
        """Returns the current TOTP code.

        Returns:
            str: TOTP code for the current time.
        """
        return self.at()

    def verify(
        self, code: str, for_time: int | None = None, window: int = 1
    ) -> bool:
        """Checks the TOTP code, taking into account the acceptable window.

        Args:
            code (str): The code entered.
            for_time (int | None, optional): Time in UNIX seconds. If None, the current time. Default is None.
            window (int, optional): Acceptable deviation in intervals (±window). Default is 1.

        Returns:
            bool: True if the code matches, otherwise False.
        """
        if for_time is None:
            for_time = int(time.time())
        for offset in range(-window, window + 1):
            if self.at(for_time + offset * self.interval) == code:
                return True
        return False
