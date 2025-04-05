# -*- coding: utf-8 -*-

import datetime
from typing import Any, Literal
from uuid import uuid4

from jam.exceptions import TokenInBlackList, TokenNotInWhiteList
from jam.jwt.lists.__abc_list_repo__ import JWTList
from jam.jwt.tools import __gen_jwt__, __validate_jwt__


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
            # "PS256",
            # "PS384",
            # "PS512",
        ] = "HS256",
        secret_key: str | None = None,
        public_key: str | None = None,
        private_key: str | None = None,
        expire: int = 3600,
        list: JWTList | None = None,
    ) -> None:
        """Class constructor.

        Args:
            alg (Literal["HS256", "HS384", "HS512", "RS256", "RS384", "RS512", "PS512", "PS384", "PS512"]): Algorithm for token encryption
            secret_key (str | None): Secret key for HMAC enecryption
            private_key (str | None): Private key for RSA enecryption
            public_key (str | None): Public key for RSA
            expire (int): Token lifetime in seconds
            list (JWTList | None): List module
        """
        super().__init__(module_type="jwt")
        self._secret_key = secret_key
        self.alg = alg
        self._private_key = (private_key,)
        self.public_key = public_key
        self.exp = expire
        self.list = list

    def make_payload(self, exp: int | None = None, **data) -> dict[str, Any]:
        """Payload maker tool.

        Args:
            exp (int | None): If none exp = JWTModule.exp
            **data: Custom data
        """
        if not exp:
            _exp = self.exp
        else:
            _exp = exp
        payload = {
            "jti": str(uuid4()),
            "exp": _exp + datetime.datetime.now().timestamp(),
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
        header = {"alg": self.alg, "typ": "jwt"}
        token = __gen_jwt__(
            header=header,
            payload=payload,
            secret=self._secret_key,
            private_key=self._private_key,  # type: ignore
        )

        if self.list:
            if self.list.__list_type__ == "white":
                self.list.add(token)
        return token

    def validate_payload(
        self, token: str, check_exp: bool = False, check_list: bool = True
    ) -> dict[str, Any]:
        """A method for verifying a token.

        Args:
            token (str): The token to check
            check_exp (bool): Check for expiration?
            check_list (bool): Check if there is a black/white list

        Raises:
            ValueError: If the token is invalid.
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None.
            EmtpyPublicKey: If RSA algorithm is selected, but public key None.
            NotFoundSomeInPayload: If 'exp' not found in payload.
            TokenLifeTimeExpired: If token has expired.
            TokenNotInWhiteList: If the list type is white, but the token is  not there
            TokenInBlackList: If the list type is black and the token is there

        Returns:
            (dict[str, Any]): Payload from token
        """
        if check_list:
            if self.list.__list_type__ == "white":  # type: ignore
                if not self.list.check(token):  # type: ignore
                    raise TokenNotInWhiteList
                else:
                    pass
            if self.list.__list_type__ == "black":  # type: ignore
                if self.list.check(token):  # type: ignore
                    raise TokenInBlackList
                else:
                    pass

        payload = __validate_jwt__(
            token=token,
            check_exp=check_exp,
            secret=self._secret_key,
            public_key=self.public_key,
        )

        return payload
