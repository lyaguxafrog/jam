# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Any, Literal

from jam.encoders import BaseEncoder, JsonEncoder
from jam.jwt.__algorithms__ import BaseAlgorithm, create_algorithm
from jam.jwt.__base__ import BaseJWT
from jam.jwt.__types__ import KeyLike
from jam.jwt.utils import base64url_decode, base64url_encode
from jam.logger import BaseLogger, logger


class JWT(BaseJWT):
    """JWT factory.

    This class provides JWT encoding and decoding functionality with support
    for multiple signing algorithms. It is designed to be easily extensible
    through inheritance and algorithm customization.

    Example:
        >>> jwt = JWT(alg="HS256", secret="my-secret-key")
        >>> token = jwt.encode({"sub": "user123"})
        >>> payload = jwt.decode(token)
    """

    _SUPPORTED_ALGORITHMS = (
        "HS256",
        "HS384",
        "HS512",
        "RS256",
        "RS384",
        "RS512",
        "ES256",
        "ES384",
        "ES512",
        "PS256",
        "PS384",
        "PS512",
    )

    def __init__(
        self,
        alg: Literal[
            "HS256",
            "HS384",
            "HS512",
            "RS256",
            "RS384",
            "RS512",
            "ES256",
            "ES384",
            "ES512",
            "PS256",
            "PS384",
            "PS512",
        ],
        secret: KeyLike,
        password: str | bytes | None = None,
        list: dict[str, Any] | None = None,
        serializer: BaseEncoder | type[BaseEncoder] = JsonEncoder,
        logger: BaseLogger = logger,
    ) -> None:
        """Initialize JWT instance.

        Args:
            alg (str): JWT algorithm name
            secret (KeyLike): Secret key for signing/verification
            password (str | bytes | None): Password for encrypted private keys
            list (dict[str, Any] | None): List config
            serializer (BaseEncoder | type[BaseEncoder]): JSON encoder/decoder
            logger (BaseLogger): Logger instance

        Raises:
            ValueError: If algorithm is not supported or secret is invalid
        """
        self._validate_algorithm(alg)
        self.alg = alg
        self._secret = secret
        self._password = self._normalize_password(password)
        self._logger = logger
        self._serializer = serializer
        self._algorithm: BaseAlgorithm | None = None
        self.list = self._list_built(list) if list else None

        self._logger.info(f"Initialized JWT with algorithm {alg}")

    def _validate_algorithm(self, alg: str) -> None:
        """Validate algorithm name.

        Args:
            alg (str): Algorithm name

        Raises:
            ValueError: If algorithm is not supported
        """
        if alg not in self._SUPPORTED_ALGORITHMS:
            raise ValueError(
                f"Unsupported algorithm: {alg}. "
                f"Supported algorithms: {', '.join(self._SUPPORTED_ALGORITHMS)}"
            )

    def _normalize_password(self, password: str | bytes | None) -> bytes | None:
        """Normalize password to bytes.

        Args:
            password (str | bytes | None): Password

        Returns:
            bytes | None: Normalized password
        """
        if password is None:
            return None
        return password.encode() if isinstance(password, str) else password

    @property
    def _algo(self) -> BaseAlgorithm:
        """Get or create algorithm instance.

        Returns:
            BaseAlgorithm: Algorithm instance
        """
        if self._algorithm is None:
            self._algorithm = create_algorithm(
                self.alg, self._secret, self._password, self._logger
            )
        return self._algorithm

    def encode(self, payload: dict[str, Any]) -> str:
        """Encode token.

        Args:
            payload (dict[str, Any]): JWT payload

        Returns:
            str: Encoded JWT token

        Raises:
            ValueError: If encoding fails
        """
        self._logger.debug(
            f"Encoding JWT with algorithm {self.alg}, payload keys: {list(payload.keys())}"
        )

        try:
            header = {"typ": "JWT", "alg": self.alg}
            header_b64 = base64url_encode(self._serializer.dumps(header))
            payload_b64 = base64url_encode(self._serializer.dumps(payload))
            data = f"{header_b64}.{payload_b64}".encode()
            self._logger.debug(
                f"JWT header and payload encoded, data length: {len(data)} bytes"
            )
            signature = self._algo.sign(data)
            token = f"{header_b64}.{payload_b64}.{signature}"

            self._logger.debug(
                f"JWT encoded successfully, token length: {len(token)} characters"
            )
            return token
        except Exception as e:
            self._logger.error(
                f"Failed to encode JWT: {e}",
                exc_info=True,
            )
            raise ValueError(f"JWT encoding failed: {e}") from e

    def decode(
        self, token: str, public_key: KeyLike | None = None
    ) -> dict[str, Any]:
        """Decode and verify token.

        Args:
            token (str): JWT token to decode
            public_key (KeyLike | None): Optional public key for verification.
                If not provided, uses the secret from initialization.

        Raises:
            ValueError: If token is invalid, malformed, or verification fails

        Returns:
            dict[str, Any]: Decoded payload
        """
        self._logger.debug(
            f"Decoding JWT token (length: {len(token)} characters)"
        )

        # Validate token format
        parts = token.split(".")
        if len(parts) != 3:
            self._logger.warning(
                f"Invalid token format: expected 3 parts, got {len(parts)}"
            )
            raise ValueError(
                "Invalid token format. Expected header.payload.signature"
            )

        try:
            h_b64, p_b64, s_b64 = parts
            self._logger.debug(
                f"Token split into parts: header={len(h_b64)} chars, payload={len(p_b64)} chars, signature={len(s_b64)} chars"
            )

            # Decode header and payload
            header = self._serializer.loads(base64url_decode(h_b64))
            payload = self._serializer.loads(base64url_decode(p_b64))
            self._logger.debug(
                f"Decoded header: {header}, payload keys: {list(payload.keys())}"
            )
            data = f"{h_b64}.{p_b64}".encode()
            sig = base64url_decode(s_b64)

            # Validate algorithm
            token_alg = header.get("alg")
            if token_alg != self.alg:
                self._logger.warning(
                    f"Algorithm mismatch: expected {self.alg}, got {token_alg}"
                )
                raise ValueError(
                    f"Algorithm mismatch: expected {self.alg}, got {token_alg}"
                )

            # Verify signature
            key = public_key or self._secret
            self._logger.debug(f"Verifying signature with algorithm {self.alg}")
            self._algo.verify(sig, data, key)

            self._logger.debug(
                f"JWT decoded and verified successfully, payload contains {len(payload)} keys"
            )
            return payload

        except ValueError:
            # Re-raise ValueError as-is (already logged)
            raise
        except Exception as e:
            self._logger.error(
                f"Failed to decode JWT: {e}",
                exc_info=True,
            )
            raise ValueError(f"JWT decoding failed: {e}") from e
