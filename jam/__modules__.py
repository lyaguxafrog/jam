# -*- coding: utf-8 -*-

import datetime
from typing import Any, Literal
from uuid import uuid4

from jam.jwt.__tools__ import __gen_jwt__, __validate_jwt__


class BaseModule:
    """The base module from which all other modules inherit."""

    def __init__(
        self,
        module_type: Literal[
            "jwt", "session-redis", "session-mongo", "session-custom"
        ],
    ) -> None:
        """Class constructor.

        Args:
            module_type (Litetal["jwt", "session-redis", "session-mongo", "session-custom"]): Type of module
        """
        self._type = module_type

    def __get_type(self) -> str:
        return self._type


class JWTModule(BaseModule):
    """Module for JWT auth.

    Methods:
        make_payload(exp: int | None, **data): Creating a generic payload for a token
    """

    def __init__(
        self,
        alg: Literal[
            "HS256",
            "HS384",
            "HS512",
            "RS256",
            "RS384",
            "RS512",
            "PS256",
            "PS384",
            "PS512",
        ] = "HS256",
        secret_key: str | None = None,
        public_key: str | None = None,
        private_key: str | None = None,
        expire: int = 3600,
    ) -> None:
        """Class constructor.

        Args:
            alg (Literal["HS256", "HS384", "HS512", "RS256", "RS384", "RS512", "PS512", "PS384", "PS512"]): Algorithm for token encryption
            secret_key (str | None): Secret key for HMAC enecryption
            private_key (str | None): Private key for RSA enecryption
            public_key (str | None): Public key for RSA
            expire (int): Token lifetime in seconds
        """
        super().__init__(module_type="jwt")
        self._secret_key = secret_key
        self.alg = alg
        self._private_key = (private_key,)
        self.public_key = public_key
        self.exp = expire

    def make_payload(self, exp: int | None = None, **data) -> dict[str, Any]:
        """Payload maker tool.

        Args:
            exp (int | None): If none exp = JWTModule.exp
            **data: Custom data
        """
        _exp = lambda e=exp: e if e is not None else self.exp  # noqa: E731
        payload = {
            "jti": str(uuid4()),
            "exp": _exp,
            "iat": datetime.datetime.now().timestamp(),
        }
        payload.update(**data)
        return payload

    def gen_token(self, **payload) -> str:
        """Creating a new token.

        Args:
            **payload: Payload with information

        Raises:
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None
            EmtpyPrivateKey: If RSA algorithm is selected, but private key None
        """
        header = {"alg": self.alg, "type": "jwt"}
        return __gen_jwt__(
            header=header,
            payload=payload,
            secret=self._secret_key,
            private_key=self._private_key,  # type: ignore
        )

    def validate_payload(
        self,
        token: str,
        check_exp: bool = False,
    ) -> dict[str, Any]:
        """A method for verifying a token.

        Args:
            token (str): The token to check
            check_exp (bool): Check for expiration?

        Raises:
            ValueError: If the token is invalid.
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None.
            EmtpyPublicKey: If RSA algorithm is selected, but public key None.
            NotFoundSomeInPayload: If 'exp' not found in payload.
            TokenLifeTimeExpired: If token has expired.

        Returns:
            (dict[str, Any]): Payload from token
        """
        return __validate_jwt__(
            token=token,
            check_exp=check_exp,
            secret=self._secret_key,
            public_key=self.public_key,
        )
