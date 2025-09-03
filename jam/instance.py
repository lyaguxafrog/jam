# -*- coding: utf-8 -*-
from collections.abc import Callable
from typing import Any, Optional, Union

from jam.__abc_instances__ import BaseJam
from jam.__logger__ import logger
from jam.modules import JWTModule, SessionModule
from jam.utils.config_maker import __config_maker__


class Jam(BaseJam):
    """Main instance."""

    def __init__(
        self,
        config: Union[dict[str, Any], str] = "pyproject.toml",
    ) -> None:
        """Class constructor.

        Args:
            config (dict[str, Any] | str): Dict or path to config file
        """
        # TODO: Refactor this to MODULES and typedict/dataclasses instances
        config = __config_maker__(config)
        otp_config = config.get("otp", None)

        if not otp_config:
            del otp_config
        else:
            from jam.otp.__abc_module__ import OTPConfig

            self._otp = OTPConfig(**otp_config)
            self._otp_module = self._otp_module_setup()
            config.pop("otp")

        self.type = config["auth_type"]
        config.pop("auth_type")
        if self.type == "jwt":
            logger.debug("Create JWT instance")
            self.module = JWTModule(**config)
        elif self.type == "session":
            logger.debug("Create Session instance")
            self.module = SessionModule(**config)  # type: ignore
        else:
            raise NotImplementedError

    # TODO: Refactor this too
    def _otp_module_setup(self) -> Callable:
        match self._otp.type:
            case "hotp":
                from jam.otp import HOTP

                return HOTP
            case "totp":
                from jam.otp import TOTP

                return TOTP
            case _:
                raise ValueError("OTP type can only be totp or hotp.")

    def _otp_checker(self) -> None:
        if not hasattr(self, "_otp"):
            raise NotImplementedError(
                "OTP not configure. Check documentation: "
            )

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

    def get_otp_code(
        self, secret: str | bytes, factor: int | None = None
    ) -> str:
        """Generates an OTP.

        Args:
            secret (str): User secret key.
            factor (int | None, optional): Unixtime for TOTP(if none, use now time) / Counter for HOTP.

        Returns:
            str: OTP code (fixed-length string).
        """
        self._otp_checker()
        return self._otp_module(
            secret=secret, digits=self._otp.digits, digest=self._otp.digest
        ).at(factor)

    def get_otp_uri(
        self,
        secret: str,
        name: Optional[str] = None,
        issuer: Optional[str] = None,
        counter: Optional[int] = None,
    ) -> str:
        """Generates an otpauth:// URI for Google Authenticator.

        Args:
            secret (str): User secret key.
            name (str): Account name (e.g., email).
            issuer (str): Service name (e.g., "GitHub").
            counter (int | None, optional): Counter (for HOTP). Default is None.

        Returns:
            str: A string of the form "otpauth://..."
        """
        self._otp_checker()
        return self._otp_module(
            secret=secret, digits=self._otp.digits, digest=self._otp.digest
        ).provisioning_uri(name, issuer, self._otp.type, counter)

    def verify_otp_code(
        self,
        secret: str,
        code: str,
        factor: Optional[int] = None,
        look_ahead: Optional[int] = 1,
    ) -> bool:
        """Checks the OTP code, taking into account the acceptable window.

        Args:
            secret (str): User secret key.
            code (str): The code entered.
            factor (int | None, optional): Unixtime for TOTP(if none, use now time) / Counter for HOTP.
            look_ahead (int, optional): Acceptable deviation in intervals (±window(totp) / ±look ahead(hotp)). Default is 1.

        Returns:
            bool: True if the code matches, otherwise False.
        """
        self._otp_checker()
        return self._otp_module(
            secret=secret, digits=self._otp.digits, digest=self._otp.digest
        ).verify(secret, code, factor, look_ahead)
