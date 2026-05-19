# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from jam.saml.types import SAMLAssertion


class BaseSAML(ABC):
    """SAML tokens module."""

    @abstractmethod
    def encode(
        self,
        *,
        subject: str,
        audience: str,
        issuer: str,
        attributes: dict[str, Any],
        expiration_seconds: int | None = 300,
    ) -> str:
        """Generate a SAML token.

        Args:
            subject (str): The subject of the token.
            audience (str): The audience of the token.
            issuer (str): The issuer of the token.
            attributes (dict[str, Any]): The attributes to include.
            expiration_seconds (int | None): Token lifetime in seconds.

        Returns:
            str: The encoded SAML token.
        """
        raise NotImplementedError

    @abstractmethod
    def decode(
        self,
        token: str,
        *,
        audience: str | None = None,
        verify_signature: bool = True,
    ) -> SAMLAssertion:
        """Decode a SAML token.

        Args:
            token (str): The SAML token to decode.
            audience (str | None): Expected audience for validation.
            verify_signature (bool): Whether to verify the signature.

        Returns:
            SAMLAssertion: The decoded assertion.

        Raises:
            JamSAMLExpired: If token is expired.
            JamSAMLNotYetValid: If token is not yet valid.
            JamSAMLInvalidAudience: If audience doesn't match.
            JamSAMLValidationError: If signature verification fails.
        """
        raise NotImplementedError

    @abstractmethod
    def validate(
        self,
        assertion: SAMLAssertion,
        *,
        audience: str | None = None,
        issuer: str | None = None,
    ) -> bool:
        """Validate a SAML assertion.

        Args:
            assertion (SAMLAssertion): The assertion to validate.
            audience (str | None): Expected audience.
            issuer (str | None): Expected issuer.

        Returns:
            bool: True if assertion is valid.

        Raises:
            JamSAMLExpired: If assertion is expired.
            JamSAMLNotYetValid: If assertion is not yet valid.
            JamSAMLInvalidAudience: If audience doesn't match.
            JamSAMLInvalidIssuer: If issuer doesn't match.
        """
        raise NotImplementedError
