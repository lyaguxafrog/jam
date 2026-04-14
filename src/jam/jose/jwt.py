# -*- coding: utf-8 -*-

from datetime import datetime
import json
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from jam.__base_encoder__ import BaseEncoder
from jam.encoders import JsonEncoder
from jam.exceptions import (
    JamJWTUnsupportedAlgorithm,
)
from jam.jose.__algorithms__ import (
    SUPPORTED_ALGORITHMS,
    SUPPORTED_ENC_ALGORITHMS,
    BaseAlgorithm,
    KeyLike,
    create_algorithm,
)
from jam.jose.__base__ import BaseJWS, BaseJWT
from jam.jose.jwe import JWE
from jam.jose.jws import JWS
from jam.jose.lists import BaseJWTList
from jam.logger import BaseLogger, logger


if TYPE_CHECKING:
    from jam.jose.jwk import JWK


class JWT(BaseJWT):
    """JWT (JSON Web Token) implementation - RFC 7519.

    Supports JWS (signed), JWE (encrypted), and JWS+JWE (sign then encrypt) tokens.
    """

    JWS = JWS
    JWE = JWE
    _SUPPORTED_ALGORITHMS = SUPPORTED_ALGORITHMS

    def __init__(
        self,
        alg: str | None = None,
        enc: str | None = None,
        secret_key: str | bytes | KeyLike | "JWK" | None = None,
        password: str | bytes | None = None,
        list: dict[str, Any] | None = None,
        serializer: BaseEncoder | type[BaseEncoder] = JsonEncoder,
        logger: BaseLogger = logger,
    ) -> None:
        """Initialize JWT instance.

        Args:
            alg (str | None): JWT algorithm name for signing (JWS). Required if encoding JWS.
            enc (str | None): JWE algorithm for encryption. If provided, creates encrypted JWT.
            secret_key (str | bytes | KeyLike | JWK | None): Key for signing/encryption.
            password (str | bytes | None): Password for encrypted private keys.
            list (dict[str, Any] | None): List config for token storage.
            serializer (BaseEncoder | type[BaseEncoder]): JSON encoder/decoder.
            logger (BaseLogger): Logger instance.

        Raises:
            ValueError: If neither alg nor enc is provided.
            JamJWTUnsupportedAlgorithm: If algorithm is not supported.
        """
        if not alg and not enc:
            raise ValueError(
                "Either 'alg' (JWS) or 'enc' (JWE) must be provided"
            )

        self._alg = alg.upper() if alg else None
        self._enc = enc.upper() if enc else None
        self._password = self._normalize_password(password)
        self._logger = logger
        self._serializer = serializer

        self._key = self._normalize_key(secret_key)
        self._algorithm: BaseAlgorithm | None = None

        if self._alg and not self._enc:
            self._validate_algorithm(self._alg)

        if self._enc:
            self._validate_enc_algorithm(self._enc)

        self.list = self._list_built(list) if list else None
        self.jws = self._build_jws() if self._alg else None
        self.jwe = self._build_jwe() if self._enc else None

        self._logger.info(f"Initialized JWT with alg={alg}, enc={enc}")

    def _normalize_key(
        self, key: str | bytes | KeyLike | "JWK" | None
    ) -> KeyLike | None:
        """Normalize key to KeyLike.

        Args:
            key: Key in various formats.

        Returns:
            KeyLike or None.
        """
        from jam.jose.jwk import JWK as JWKClass

        if key is None:
            return None
        if isinstance(key, JWKClass):
            return key._to_keylike()
        if isinstance(key, str):
            return key.encode() if key else key
        return key

    def _build_jws(self) -> BaseJWS:
        if not self._alg or not self._key:
            raise ValueError("JWS requires 'alg' and 'key'")

        jws_alg = self._alg
        jws_key = self._key

        # TODO: Optimize this
        if self._enc and jws_alg in (
            "RS256",
            "RS384",
            "RS512",
            "ES256",
            "ES384",
            "ES512",
            "PS256",
            "PS384",
            "PS512",
            "RSA-OAEP",
        ):
            jws_alg = "RS256"

        return self.JWS(
            alg=jws_alg,
            key=jws_key,
            password=self._password,
            logger=self._logger,
        )

    def _build_jwe(self) -> JWE:
        if not self._enc or not self._key:
            raise ValueError("JWE requires 'enc' and 'key'")

        alg = self._alg
        enc_key = self._key

        if not alg:
            key_len = len(self._key) if isinstance(self._key, bytes) else 16
            alg = "A256KW" if key_len >= 32 else "A128KW"
        elif alg in ("HS256", "HS384", "HS512"):
            alg = "A256KW" if len(self._key) >= 32 else "A128KW"
            enc_key = self._derive_encryption_key(self._key)
        elif alg in (  # TODO: and this
            "RS256",
            "RS384",
            "RS512",
            "ES256",
            "ES384",
            "ES512",
            "PS256",
            "PS384",
            "PS512",
        ):
            alg = "RSA-OAEP"

        return self.JWE(
            alg=alg,
            enc=self._enc,
            key=enc_key,
            password=self._password,
            serializer=self._serializer,
            logger=self._logger,
        )

    def _derive_encryption_key(self, signing_key: bytes) -> bytes:
        """Derive encryption key from signing key using HKDF.

        Args:
            signing_key: The signing key.

        Returns:
            32-byte encryption key.
        """
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF

        return HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"jwe-encryption",
            info=b"encryption-key",
        ).derive(signing_key)

    def _list_built(self, list_config: dict[str, Any]) -> BaseJWTList:
        """Builder list."""
        match list_config["backend"]:
            case "redis":
                from jam.jose.lists.redis import RedisList

                return RedisList(
                    type=list_config.get("type", "black"),
                    prefix=list_config.get("prefix", "jwt_list"),
                    redis_uri=list_config.get("redis_uri"),
                    ttl=list_config.get("ttl"),
                )
            case "json":
                from jam.jose.lists.json import JSONList

                return JSONList(
                    type=list_config.get("type", "black"),
                    prefix=list_config.get("prefix", "jwt_list"),
                    json_path=list_config.get("json_path", "whitelist.json"),
                )
            case "memory":
                from jam.jose.lists.memory import MemoryList

                return MemoryList(
                    type=list_config.get("type", "black"),
                    prefix=list_config.get("prefix", "jwt_list"),
                )
            case _:
                raise ValueError(
                    f"Unknown list backend: {list_config['backend']}"
                )

    def _validate_algorithm(self, alg: str) -> None:
        """Validate JWS algorithm."""
        if alg not in self._SUPPORTED_ALGORITHMS:
            raise JamJWTUnsupportedAlgorithm(
                details={
                    "algorithm": alg,
                    "supported_algorithms": self._SUPPORTED_ALGORITHMS,
                }
            )

    def _validate_enc_algorithm(self, enc: str) -> None:
        """Validate JWE encryption algorithm."""
        if enc not in SUPPORTED_ENC_ALGORITHMS:
            raise JamJWTUnsupportedAlgorithm(
                details={
                    "algorithm": enc,
                    "supported_algorithms": SUPPORTED_ENC_ALGORITHMS,
                }
            )

    def _normalize_password(self, password: str | bytes | None) -> bytes | None:
        """Normalize password to bytes."""
        if password is None:
            return None
        return password.encode() if isinstance(password, str) else password

    @property
    def _algo(self) -> BaseAlgorithm:
        """Get or create algorithm instance."""
        if self._algorithm is None:
            if not self._alg or not self._key:
                raise ValueError("JWS requires 'alg' and 'key'")
            self._algorithm = create_algorithm(
                self._alg, self._key, self._password, self._logger
            )
        return self._algorithm

    def _make_payload(
        self,
        iss: str | None,
        sub: str | None,
        aud: str | None,
        exp: int | None,
        nbf: int | None,
        data: dict[str, Any] | None,
    ) -> dict[str, Any]:
        now = int(datetime.now().timestamp())
        payload = {
            "tid": str(uuid4()),
            "iat": now,
            "iss": iss,
            "sub": sub,
            "aud": aud,
            "exp": now + exp if exp else None,
            "nbf": now + nbf if nbf is not None else None,
        }
        if data:
            payload.update(data)
        payload = {k: v for k, v in payload.items() if v is not None}
        return payload

    def encode(
        self,
        iss: str | None = None,
        sub: str | None = None,
        aud: str | None = None,
        exp: int | None = None,
        nbf: int | None = None,
        header: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> str:
        """Encode the JWT with the given expire, header, and payload (JWS).

        Args:
            exp (int | None): The expiration time in seconds.
            nbf (int | None): The not-before time in seconds.
            iss (str | None): The issuer.
            sub (str | None): The subject.
            aud (str | None): The audience.
            header (dict[str, Any] | None): The header to include in the JWT.
            payload (dict[str, Any] | None): The payload to include in the JWT.

        Returns:
            str: The encoded JWT (JWS compact serialization).

        Raises:
            ValueError: If alg is not provided.
        """
        if not self.jws:
            raise ValueError("JWS not configured. Provide 'alg' parameter.")

        _base_header = {"alg": self._alg, "typ": "JWT"}
        if header:
            _base_header.update(header)
        _payload = self._make_payload(iss, sub, aud, exp, nbf, payload)
        return self.jws.sign(header=_base_header, data=_payload)

    def decode(
        self,
        token: str,
        include_headers: bool = False,
    ) -> dict[str, Any]:
        """Decode the JWT and return the payload (JWS).

        Args:
            token (str): The JWT to decode.
            exp (bool): Whether to check the expiration time. Defaults to False.
            nbf (bool): Whether to check the not-before time. Defaults to False.
            include_headers (bool): Whether to include the headers in the result. Defaults to False.
            check_list (bool): Whether to check token in list. Defaults to False.

        Returns:
            dict[str, Any]: The decoded payload.

        Raises:
            ValueError: If alg is not provided.
        """
        if not self.jws:
            raise ValueError("JWS not configured. Provide 'alg' parameter.")

        data = self.jws.verify(token, True)
        header = data["header"]
        if header.get("typ") != "JWT":
            raise ValueError("Invalid token type")
        if include_headers:
            return data
        return data["payload"]

    def encrypt(
        self,
        payload: dict[str, Any] | str,
        header: dict[str, Any] | None = None,
    ) -> str:
        """Encrypt payload using JWE.

        If both alg and enc are provided, creates JWS+JWE (sign then encrypt):
        1. Create JWS compact serialization (sign)
        2. Use JWS result as plaintext for JWE (encrypt)

        Args:
            payload: Data to encrypt. If dict, will be JSON encoded.
            header: Additional JWE header.

        Returns:
            str: Encrypted JWT (JWE or JWS+JWE).

        Raises:
            ValueError: If enc is not provided.
        """
        if not self.jwe:
            raise ValueError("JWE not configured. Provide 'enc' parameter.")

        if isinstance(payload, dict):
            payload_bytes = self._serializer.dumps(payload)
        elif isinstance(payload, str):
            payload_bytes = payload.encode("utf-8")
        else:
            payload_bytes = payload

        if self._alg and self._enc:
            _base_header = {"alg": self._alg, "typ": "JWT"}
            if header:
                _base_header.update(header)
            jws_payload = self.jws.sign(header=_base_header, data=payload_bytes)
            return self.jwe.encrypt(jws_payload, header)
        else:
            return self.jwe.encrypt(payload_bytes, header)

    def decrypt(self, token: str) -> dict[str, Any]:
        """Decrypt JWE or JWS+JWE token.

        If token is JWS+JWE (sign then encrypt):
        1. Decrypt JWE to get JWS compact serialization
        2. Verify JWS to get original payload

        Args:
            token: Encrypted JWT token.

        Returns:
            dict[str, Any]: Decrypted payload.

        Raises:
            ValueError: If enc is not provided or decryption fails.
        """
        if not self.jwe:
            raise ValueError("JWE not configured. Provide 'enc' parameter.")

        plaintext = self.jwe.decrypt(token)

        if self._alg:
            if isinstance(plaintext, bytes):
                plaintext = plaintext.decode("utf-8")

            alg = self._alg
            if alg in (  # TODO: and this
                "RS256",
                "RS384",
                "RS512",
                "ES256",
                "ES384",
                "ES512",
                "PS256",
                "PS384",
                "PS512",
                "RSA-OAEP",
            ):
                alg = "RS256"

            original_alg = self.jws._alg
            original_key = self.jws._key
            self.jws._alg = alg
            try:
                decoded = self.jws.verify(plaintext, True)
                payload = decoded.get("payload")
                if isinstance(payload, bytes):
                    return self._serializer.loads(payload)
                return decoded
            finally:
                self.jws._alg = original_alg
                self.jws._key = original_key

        try:
            return self._serializer.loads(plaintext)
        except (json.JSONDecodeError, UnicodeDecodeError):
            if isinstance(plaintext, bytes):
                plaintext = plaintext.decode("utf-8")
            return {"raw": plaintext}
