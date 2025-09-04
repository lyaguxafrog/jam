# -*- coding: utf-8 -*-

from jam.otp.__abc_module__ import BaseOTP


class HOTP(BaseOTP):
    """HOTP instance."""

    def at(self, factor: int) -> str:
        """Generates a HOTP code for the specified counter.

        Args:
            factor (int): Counter (increases after each use).

        Returns:
            str: HOTP code (fixed-length string).
        """
        return str(self._dynamic_truncate(self._hmac(factor))).zfill(
            self.digits
        )

    def verify(self, code: str, factor: int, look_ahead: int = 1) -> bool:
        """Verify HOTP-code.

        Args:
            code (str): Code.
            factor (int): Now counter.
            look_ahead (int, optional): Allowable forward offset (to compensate for desynchronization). Default is 1..

        Returns:
            bool: True if the code matches, otherwise False.
        """
        for i in range(factor, factor + look_ahead + 1):
            if self.at(i) == code:
                return True
        return False
