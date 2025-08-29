# -*- coding: utf-8 -*-

from typing import Any, Literal, Optional

from jam.__abc_instances__ import __AbstractInstance
from jam.__logger__ import logger
from jam.modules import JWTModule, SessionModule


class Jam(__AbstractInstance):
    """Main instance."""

    def __init__(
        self,
        auth_type: Literal["jwt", "session"],
        config: dict[str, Any],
    ) -> None:
        """Class constructor.

        Args:
            auth_type (Literal["jwt", "sessions"]): Type of auth*
            config (dict[str, Any] | str): Config for Jam, can use `jam.utils.config_maker`
        """
        # TODO: Refactor this to MODULES and typedict/dataclasses instances
        self.type = auth_type
        if self.type == "jwt":
            logger.debug("Create JWT instance")
            self.module = JWTModule(
                alg=config["alg"],
                secret_key=config["secret_key"],
                private_key=config["private_key"],
                public_key=config["public_key"],
                expire=config["expire"],
                list=config["list"],
            )
        elif self.type == "session":
            logger.debug("Create Session instance")
            self.module = SessionModule(**config)  # type: ignore
        else:
            raise NotImplementedError

    def gen_jwt_token(self, payload: dict[str, Any]) -> str:
        """Creating a new token.

        Args:
            payload (dict[str, Any]): Payload with information

        Raises:
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None
            EmtpyPrivateKey: If RSA algorithm is selected, but private key None
        """
        if self.type != "jwt":
            raise NotImplementedError(
                "This method is only available for JWT auth*."
            )

        return self.module.gen_token(**payload)

    def verify_jwt_token(
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

        return self.module.validate_payload(
            token=token, check_exp=check_exp, check_list=check_list
        )

    def make_payload(self, exp: int | None = None, **data) -> dict[str, Any]:
        """Payload maker tool.

        Args:
            exp (int | None): If none exp = JWTModule.exp
            **data: Custom data
        """
        if self.type != "jwt":
            raise NotImplementedError(
                "This method is only available for JWT auth*."
            )

        return self.module.make_payload(exp=exp, **data)

    def create_session(self, session_key: str, data: dict) -> str:
        """Create a new session.

        Args:
            session_key (str): Session key
            data (dict): Data to store in session

        Raises:
            NotImplementedError: If the auth type is not "session"

        Returns:
            str: The created session key
        """
        if self.type != "session":
            raise NotImplementedError(
                "This method is only available for Session auth*."
            )
        return self.module.create(session_key, data)

    def get_session(self, session_id: str) -> Optional[dict]:
        """Retrieve session data by session ID.

        Args:
            session_id (str): The ID of the session to retrieve.

        Raises:
            NotImplementedError: If the auth type is not "session".

        Returns:
            dict | None: The session data if found, otherwise None.
        """
        if self.type != "session":
            raise NotImplementedError(
                "This method is only available for Session auth*."
            )
        return self.module.get(session_id)

    def delete_session(self, session_id: str) -> None:
        """Delete a session by its ID.

        Args:
            session_id (str): The ID of the session to delete.

        Raises:
            NotImplementedError: If the auth type is not "session".

        Returns:
            None
        """
        if self.type != "session":
            raise NotImplementedError(
                "This method is only available for Session auth*."
            )
        return self.module.delete(session_id)

    def update_session(self, session_id: str, data: dict) -> None:
        """Update session data by session ID.

        Args:
            session_id (str): The ID of the session to update.
            data (dict): The new data to update the session with.

        Raises:
            NotImplementedError: If the auth type is not "session".

        Returns:
            None
        """
        if self.type != "session":
            raise NotImplementedError(
                "This method is only available for Session auth*."
            )
        return self.module.update(session_id, data)

    def clear_sessions(self, session_key: str) -> None:
        """Clear all sessions associated with a specific session key.

        Args:
            session_key (str): The session key whose sessions are to be cleared.

        Raises:
            NotImplementedError: If the auth type is not "session".

        Returns:
            None
        """
        if self.type != "session":
            raise NotImplementedError(
                "This method is only available for Session auth*."
            )
        return self.module.clear(session_key)

    def rework_session(self, old_session_key: str) -> str:
        """Rework an existing session key to a new one.

        Args:
            old_session_key (str): The old session key to be reworked.

        Raises:
            NotImplementedError: If the auth type is not "session".

        Returns:
            str: The new session key.
        """
        if self.type != "session":
            raise NotImplementedError(
                "This method is only available for Session auth*."
            )
        return self.module.rework(old_session_key)
