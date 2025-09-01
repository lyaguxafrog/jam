# -*- coding: utf-8 -*-

import datetime
from typing import Any, Literal
from uuid import uuid4

from jam.aio.jwt.lists.json import JSONList
from jam.aio.jwt.lists.redis import RedisList
from jam.aio.jwt.tools import __gen_jwt_async__, __validate_jwt_async__
from jam.exceptions import TokenInBlackList, TokenNotInWhiteList
from jam.modules import BaseModule
from jam.utils.config_maker import __module_loader__


class JWTModule(BaseModule):
    """Module for JWT auth."""

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
        list: dict[str, Any] | None = None,
    ) -> None:
        """Class constructor.

        Args:
            alg (Literal["HS256", "HS384", "HS512", "RS256", "RS384", "RS512", "PS512", "PS384", "PS512"]): Algorithm for token encryption
            secret_key (str | None): Secret key for HMAC enecryption
            private_key (str | None): Private key for RSA enecryption
            public_key (str | None): Public key for RSA
            expire (int): Token lifetime in seconds
            list (dict[str, Any]): List config
        """
        super().__init__(module_type="jwt")
        self._secret_key = secret_key
        self.alg = alg
        self._private_key = private_key
        self.public_key = public_key
        self.exp = expire

        self.list = None
        if list is not None:
            self.list = self._init_list(list)

    @staticmethod
    def _init_list(config: dict[str, Any]):
        match config["backend"]:
            case "redis":
                return RedisList(
                    type=config["type"],
                    redis_uri=config["redis_uri"],
                    in_list_life_time=config["in_list_life_time"],
                )
            case "json":
                return JSONList(
                    type=config["type"], json_path=config["json_path"]
                )
            case "custom":
                module = __module_loader__(config["custom_module"])
                cfg = dict(config)
                cfg.pop("type")
                cfg.pop("custom_module")
                cfg.pop("backend")
                return module(**cfg)
            case _:
                raise ValueError(f"Unknown list_type: {config['list_type']}")

    async def make_payload(
        self, exp: int | None = None, **data
    ) -> dict[str, Any]:
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

    async def gen_token(self, **payload) -> str:
        """Creating a new token.

        Args:
            **payload: Payload with information

        Raises:
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None
            EmtpyPrivateKey: If RSA algorithm is selected, but private key None
        """
        header = {"alg": self.alg, "typ": "jwt"}
        token = await __gen_jwt_async__(
            header=header,
            payload=payload,
            secret=self._secret_key,
            private_key=self._private_key,
        )

        if self.list:
            if self.list.__list_type__ == "white":
                await self.list.add(token)
        return token

    async def validate_payload(
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
                if not await self.list.check(token):  # type: ignore
                    raise TokenNotInWhiteList
                else:
                    pass
            if self.list.__list_type__ == "black":  # type: ignore
                if await self.list.check(token):  # type: ignore
                    raise TokenInBlackList
                else:
                    pass

        payload = __validate_jwt_async__(
            token=token,
            check_exp=check_exp,
            secret=self._secret_key,
            public_key=self.public_key,
        )

        return await payload
