# -*- coding: utf-8 -*-

from typing import Any

from jam.__abc_instances__ import AbstractInstance
from jam.__modules__ import JWTModule


class Jam(AbstractInstance):
    """Main instance."""

    def __init__(
            self,
            auth_type: str,
            config: dict[str, Any]
    ) -> None:
        """Class construcotr.

        Args:
            auth_type (str): Type of auth*
            config (dict[str, Any]): Config for Jam, can use `jam.utils.config_maker`
        """
        self.type = auth_type
        if self.type == "jwt":
            self.module = JWTModule(
                alg=config["alg"],
                secret_key=config["secret_key"],
                public_key=config["public_key"],
                private_key=config["private_key"],
                expire=config["expire"]
            )
        else:
            raise NotImplementedError


    def gen_jwt_token(self, **payload) -> str:
        """Creating a new token.

        Args:
            **payload: Payload with information

        Raises:
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None
            EmtpyPrivateKey: If RSA algorithm is selected, but private key None
        """
        return self.module.gen_token(**payload)

    def verify_jwt_token(
            self,
            token: str,
            check_exp: bool = True
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
        return self.module.validate_payload(
            token=token, check_exp=check_exp
        )

    def make_payload(self, exp: int | None = None, **data) -> dict[str, Any]:
        """Payload maker tool.

        Args:
            exp (int | None): If none exp = JWTModule.exp
            **data: Custom data
        """
        return self.module.make_payload(exp=exp, **data)