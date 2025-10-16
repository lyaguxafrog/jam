# -*- coding: utf-8 -*-


from typing import Any, Literal, Optional, Union

from jam.__abc_encoder__ import BaseEncoder
from jam.encoders import JsonEncoder

from .__abc_paseto_repo__ import PASETO, BasePASETO


class PASETOv1(BasePASETO):
    """Paseto v1 factory."""

    _VERSION = "v1"

    @classmethod
    def key(
        cls: type[PASETO],
        purpose: Literal["local", "public"],
        key: Union[str, bytes],
    ) -> PASETO:
        """Return PASETO instance.

        Args:
            purpose (Literal["local", "public"]): Paseto purpose
            key (str | bytes): PEM or secret key

        Returns:
            PASETO: Paseto instance
        """
        ky = cls()
        ky._secret = key
        ky._purpose = purpose
        return ky

    def encode(
        self,
        payload: dict[str, Any],
        footer: Optional[Union[dict[str, Any], str]] = None,
        serializer: BaseEncoder = JsonEncoder,
    ) -> str:
        """Encode PASETO."""
        ...

    @staticmethod
    def decode(
        token: str,
        public_key: Optional[str] = None,
        serializer: BaseEncoder = JsonEncoder,
    ) -> dict[str, Any]:
        """Decide PASETO."""
        ...
