# -*- coding: utf-8 -*-

from typing import Any, Literal

from jam.__abc_instances__ import __AbstractInstance
from jam.aio.modules import JWTModule


class Jam(__AbstractInstance):
    """Main instance for aio."""

    def __init__(
        self, auth_type: Literal["jwt"], config: dict[str, Any]
    ) -> None:
        """Class constructor.

        Args:
            auth_type (str): Type of auth*
            config (dict[str, Any] | str): Config for Jam, can use `jam.utils.config_maker`
        """
        self.type = auth_type
        if self.type == "jwt":
            self.module = JWTModule(
                alg=config["alg"],
                secret_key=config["secret_key"],
                private_key=config["private_key"],
                public_key=config["public_key"],
                expire=config["expire"],
                list=config["list"],
            )
        else:
            raise NotImplementedError

    async def gen_jwt_token(self, payload: dict[str, Any]) -> str:
        """Creating a new token.

        Args:
            payload (dict[str, Any]): Payload with information

        Raises:
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None
            EmtpyPrivateKey: If RSA algorithm is selected, but private key None

        Returns:
            (str): Generated token
        """
        if self.type != "jwt":
            raise NotImplementedError(
                "This method is only available for JWT auth*."
            )

        token: str = await self.module.gen_token(**payload)
        return token

    async def verify_jwt_token(
        self, token: str, check_exp: bool = True, check_list: bool = True
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
        if self.type != "jwt":
            raise NotImplementedError(
                "This method is only available for JWT auth*."
            )

        return await self.module.validate_payload(
            token=token, check_exp=check_exp, check_list=check_list
        )

    async def make_payload(
        self, exp: int | None = None, **data
    ) -> dict[str, Any]:
        """Payload maker tool.

        Args:
            exp (int | None): If none exp = JWTModule.exp
            **data: Custom data
        """
        if self.type != "jwt":
            raise NotImplementedError(
                "This method is only available for JWT auth*."
            )

        return await self.module.make_payload(exp=exp, **data)
