# -*- coding: utf-8 -*-

from typing import Any, Union

from jam.__abc_instances__ import BaseJam
from jam.aio.modules import JWTModule
from jam.utils.config_maker import __config_maker__


class Jam(BaseJam):
    """Main instance for aio."""

    def __init__(
        self, config: Union[dict[str, Any], str] = "pyproject.toml"
    ) -> None:
        """Class constructor.

        Args:
            config (dict[str, Any] | str): Config for Jam, can use `jam.utils.config_maker`
        """
        config = __config_maker__(config)
        self.type = config["auth_type"]
        config.pop("auth_type")
        if self.type == "jwt":
            self.module = JWTModule(**config)
        elif self.type == "session":
            raise NotImplementedError(
                "Asynchronous methods are not yet \
                implemented in this version. \
                Please check for updates at https://github.com/lyaguxafrog/jam/releases"
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

    async def create_session(self, session_key: str, data: dict) -> str:
        """Create new session."""
        raise NotImplementedError(
            "Asynchronous methods are not yet implemented in this version. Please check for updates at https://github.com/lyaguxafrog/jam/releases"
        )

    async def get_session(self, session_id: str) -> dict | None:
        """Retrieve session data by session ID."""
        raise NotImplementedError(
            "Asynchronous methods are not yet implemented in this version. Please check for updates at https://github.com/lyaguxafrog/jam/releases"
        )

    async def delete_session(self, session_id: str) -> None:
        """Delete a session by its ID."""
        raise NotImplementedError(
            "Asynchronous methods are not yet implemented in this version. Please check for updates at https://github.com/lyaguxafrog/jam/releases"
        )

    async def update_session(self, session_id: str, data: dict) -> None:
        """Update session data by session ID."""
        raise NotImplementedError(
            "Asynchronous methods are not yet implemented in this version. Please check for updates at https://github.com/lyaguxafrog/jam/releases"
        )

    async def clear_sessions(self, session_key: str) -> None:
        """Clear all sessions associated with a specific session key."""
        raise NotImplementedError(
            "Asynchronous methods are not yet implemented in this version. Please check for updates at https://github.com/lyaguxafrog/jam/releases"
        )

    async def rework_session(self, old_session_key: str) -> str:
        """Rework an existing session key to a new one."""
        raise NotImplementedError(
            "Asynchronous methods are not yet implemented in this version. Please check for updates at https://github.com/lyaguxafrog/jam/releases"
        )
