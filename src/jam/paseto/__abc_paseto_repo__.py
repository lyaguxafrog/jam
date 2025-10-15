# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Literal, Optional, TypeVar, Union

from jam.__abc_encoder__ import BaseEncoder
from jam.encoders import JsonEncoder


PASETO = TypeVar("PASETO", bound="BasePASETO")


class BasePASETO(ABC):
    """Base PASETO instance."""

    _VERSION: str

    def __init__(self):
        """Constructor."""
        self._secret: Optional[str] = None
        self._purpose: Optional[Literal["local", "public"]] = None

    @property
    def purpose(self) -> Optional[Literal["local", "public"]]:
        """Return PASETO purpose."""
        return self._purpose

    @classmethod
    @abstractmethod
    def key(
        cls: type[PASETO],
        purpose: Literal["local", "public"],
        key: Union[str, bytes],
    ) -> PASETO:
        """Create a PASETO instance with the given key.

        Args:
            purpose: 'local' (symmetric encryption) or 'public' (asymmetric signing)
            key: raw bytes or PEM text depending on purpose

        Returns:
            PASETO: configured PASETO instance for encoding/decoding tokens.
        """
        raise NotImplementedError

    @abstractmethod
    def encode(
        self,
        payload: dict[str, Any],
        footer: Optional[Union[dict[str, Any], str]] = None,
        serializer: BaseEncoder = JsonEncoder,
    ) -> str:
        """Generate token from key instance.

        Args:
            payload (dict[str, Any]): Payload for token
            footer (dict[str, Any] | str  | None): Token footer
            serializer (BaseEncoder): JSON Encoder
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def decode(
        token: str,
        public_key: Optional[str] = None,
        serializer: BaseEncoder = JsonEncoder,
    ) -> dict[str, Any]:
        """Decode PASETO.

        Args:
            token (str): Token
            public_key (str | None): Public key if needed
            serializer (BaseEncoder): JSON Encoder

        Returns:
            dict[str, Any]: Payload
        """
        raise NotImplementedError
