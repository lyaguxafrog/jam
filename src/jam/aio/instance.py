# -*- coding: utf-8 -*-

import gc
from collections.abc import Callable
from typing import Any, Optional, Union

from jam.__abc_instances__ import BaseJam
from jam.__deprecated__ import deprecated
from jam.__logger__ import logger
from jam.aio.modules import JWTModule, OAuth2Module, SessionModule
from jam.utils.config_maker import __config_maker__, __module_loader__


class Jam(BaseJam):
    """Main instance for aio."""

    _JAM_MODULES: dict[str, str] = {
        "jwt": "jam.aio.modules.JWTModule",
        "session": "jam.aio.modules.SessionModule",
        "oauth2": "jam.aio.modules.OAuth2Module",
    }

    def __init__(
        self,
        config: Union[dict[str, Any], str] = "pyproject.toml",
        pointer: str = "jam",
    ) -> None:
        """Class constructor.

        Args:
            config (dict[str, Any] | str): dict or path to config file
            pointer (str): Config read point
        """
        self.jwt: Optional[JWTModule] = None
        self.session: Optional[SessionModule] = None
        self.oauth2: Optional[OAuth2Module] = None

        config = __config_maker__(config, pointer)

        # OTP
        otp_config = config.pop("otp", None)
        if otp_config:
            from jam.otp.__abc_module__ import OTPConfig

            self._otp = OTPConfig(**otp_config)
            self._otp_module = self._otp_module_setup()
            logger.debug("OTP module initialized")

        # Other modules
        if config.get("auth_type", None):
            logger.warning(
                "This configuration type is deprecated, see: https://jam.makridenko.ru/config"
            )
            name = config.pop("auth_type")
            module = __module_loader__(self._JAM_MODULES[name])
            self.module = module
            setattr(self, name, module(**config))
        else:
            for name, cfg in config.items():
                try:
                    module = self.build_module(name, cfg)
                    if name == "jwt":
                        self.module = module
                    setattr(self, name, module)
                    logger.debug(
                        f"Auth module '{name}' successfully initialized"
                    )
                except Exception as e:
                    logger.exception(
                        f"Failed to initialize auth module '{name}': {e}"
                    )
        gc.collect()

    def _otp_module_setup(self) -> Callable:
        otp_type = self._otp.type
        if otp_type == "hotp":
            from jam.otp import HOTP

            return HOTP
        elif otp_type == "totp":
            from jam.otp import TOTP

            return TOTP
        else:
            raise ValueError("OTP type can only be totp or hotp.")

    def _otp_checker(self) -> None:
        if not hasattr(self, "_otp"):
            raise NotImplementedError(
                "OTP not configure. Check documentation: "
            )

    async def jwt_make_payload(
        self, exp: Optional[int], data: dict[str, Any]
    ) -> dict[str, Any]:
        """Make JWT-specific payload.

        Args:
            exp (int | None): Token expire, if None -> use default
            data (dict[str, Any]): Data to payload

        Returns:
            dict[str, Any]: Payload
        """
        return await self.jwt.make_payload(exp=exp, **data)

    async def jwt_create_token(self, payload: dict[str, Any]) -> str:
        """Create JWT token.

        Args:
            payload (dict[str, Any]): Data payload

        Returns:
            str: New token

        Raises:
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None
            EmtpyPrivateKey: If RSA algorithm is selected, but private key None
        """
        return await self.jwt.gen_token(**payload)

    async def jwt_verify_token(
        self, token: str, check_exp: bool = True, check_list: bool = True
    ) -> dict[str, Any]:
        """Verify and decode JWT token.

        Args:
            token (str): JWT token
            check_exp (bool): Check expire
            check_list (bool): Check white/black list. Docs: https://jam.makridenko.ru/jwt/lists/what/

        Returns:
            dict[str, Any]: Decoded payload

        Raises:
            ValueError: If the token is invalid.
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None.
            EmtpyPublicKey: If RSA algorithm is selected, but public key None.
            NotFoundSomeInPayload: If 'exp' not found in payload.
            TokenLifeTimeExpired: If token has expired.
            TokenNotInWhiteList: If the list type is white, but the token is  not there
            TokenInBlackList: If the list type is black and the token is there
        """
        return await self.jwt.validate_payload(token, check_exp, check_list)

    async def session_create(
        self, session_key: str, data: dict[str, Any]
    ) -> str:
        """Create new session.

        Args:
            session_key (str): Key for session
            data (dict[str, Any]): Session data

        Returns:
            str: New session ID
        """
        return await self.session.create(session_key, data)

    async def session_get(self, session_id: str) -> Optional[dict[str, Any]]:
        """Get data from session.

        Args:
            session_id (str): Session ID

        Returns:
            dict[str, Any] | None: Session data if exist
        """
        return await self.session.get(session_id)

    async def session_delete(self, session_id: str) -> None:
        """Delete session.

        Args:
            session_id (str): Session ID
        """
        return await self.session.delete(session_id)

    async def session_update(
        self, session_id: str, data: dict[str, Any]
    ) -> None:
        """Update session data.

        Args:
            session_id (str): Session ID
            data (dict[str, Any]): New data
        """
        return await self.session.update(session_id, data)

    async def session_clear(self, session_key: str) -> None:
        """Delete all sessions by key.

        Args:
            session_key (str): Key of session
        """
        return await self.session.clear(session_key)

    async def session_rework(self, old_session_id: str) -> str:
        """Rework session.

        Args:
            old_session_id (str): Old session id

        Returns:
            str: New session id
        """
        return await self.session.rework(old_session_id)

    def otp_code(
        self, secret: Union[str, bytes], factor: Optional[int] = None
    ) -> str:
        """Generates an OTP.

        Args:
            secret (str | bytes): User secret key.
            factor (int | None, optional): Unixtime for TOTP(if none, use now time) / Counter for HOTP.

        Returns:
            str: OTP code (fixed-length string).
        """
        self._otp_checker()
        return self._otp_module(
            secret=secret, digits=self._otp.digits, digest=self._otp.digest
        ).at(factor)

    def otp_uri(
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
        ).provisioning_uri(
            name=name, issuer=issuer, type_=self._otp.type, counter=counter
        )

    def otp_verify_code(
        self,
        secret: Union[str, bytes],
        code: str,
        factor: Optional[int] = None,
        look_ahead: Optional[int] = 1,
    ) -> bool:
        """Checks the OTP code, taking into account the acceptable window.

        Args:
            secret (str | bytes): User secret key.
            code (str): The code entered.
            factor (int | None, optional): Unixtime for TOTP(if none, use now time) / Counter for HOTP.
            look_ahead (int, optional): Acceptable deviation in intervals (±window(totp) / ±look ahead(hotp)). Default is 1.

        Returns:
            bool: True if the code matches, otherwise False.
        """
        self._otp_checker()
        return self._otp_module(
            secret=secret, digits=self._otp.digits, digest=self._otp.digest
        ).verify(code=code, factor=factor, look_ahead=look_ahead)

    @deprecated("This method is deprecated, use: Jam.jwt_create_token")
    async def gen_jwt_token(self, payload: dict[str, Any]) -> str:
        """Creating a new token.

        Args:
            payload (dict[str, Any]): Payload with information

        Deprecated:
            Use: `Jam.jwt_create_token`

        Raises:
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None
            EmtpyPrivateKey: If RSA algorithm is selected, but private key None

        Returns:
            (str): Generated token
        """
        return await self.jwt.gen_token(**payload)

    @deprecated("This method is deprecated, use: Jam.jwt_verify_token")
    async def verify_jwt_token(
        self, token: str, check_exp: bool = True, check_list: bool = True
    ) -> dict[str, Any]:
        """A method for verifying a token.

        Args:
            token (str): The token to check
            check_exp (bool): Check for expiration?
            check_list (bool): Check if there is a black/white list

        Deprecated:
            Use: `Jam.jwt_verify_token`

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
        return await self.jwt.validate_payload(
            token=token, check_exp=check_exp, check_list=check_list
        )

    @deprecated("This method is deprecated, use: Jam.jwt_make_payload")
    async def make_payload(
        self, exp: Optional[int] = None, **data: Any
    ) -> dict[str, Any]:
        """Payload maker tool.

        Args:
            exp (int | None): If none exp = JWTModule.exp
            **data: Custom data

        Deprecated:
            Use: `Jam.jwt_make_payload`
        """
        return await self.jwt.make_payload(exp=exp, **data)

    @deprecated("This method is deprecated, use: `Jam.session_create`")
    async def create_session(
        self, session_key: str, data: dict[str, Any]
    ) -> str:
        """Create new session.

        Args:
            session_key (str): Key for sessions
            data (dict[str, Any]): Session payload

        Deprecated:
            Use: `Jam.session_create`

        Returns:
            str: New session ID
        """
        return await self.session.create(session_key, data)

    @deprecated("This method is deprecates, use: Jam.session_get")
    async def get_session(self, session_id: str) -> Optional[dict[str, Any]]:
        """Retrieve session data by session ID.

        Args:
            session_id (str): Session ID

        Deprecated:
            Use: `Jam.session_get`

        Returns:
            dict | None: Session payload if exists
        """
        return await self.session.get(session_id)

    @deprecated("This method is deprecated, use: Jam.session_delete")
    async def delete_session(self, session_id: str) -> None:
        """Delete a session by its ID.

        Args:
            session_id (str): Session ID

        Deprecated:
            Use: `Jam.session_delete`

        Returns:
            None
        """
        return await self.session.delete(session_id)

    @deprecated("This method is deprecated, use: Jam.session_update")
    async def update_session(
        self, session_id: str, data: dict[str, Any]
    ) -> None:
        """Update session data by session ID.

        Args:
            session_id (str): Session ID
            data (dict[str, Any]): Data for update

        Deprecated:
            Use: `Jam.session_update`

        Returns:
            None
        """
        return await self.session.update(session_id, data)

    @deprecated("This method is deprecated, use: Jam.session_clear")
    async def clear_sessions(self, session_key: str) -> None:
        """Clear all sessions associated with a specific session key.

        Args:
            session_key (str): Key for session scope

        Deprecated:
            Use: `Jam.session_clear`

        Returns:
            None
        """
        return await self.session.clear(session_key)

    @deprecated("This method is deprecated, use: Jam.session_rework")
    async def rework_session(self, old_session_key: str) -> str:
        """Rework an existing session key to a new one.

        Args:
            old_session_key (str): Rework session

        Deprecated:
            Use: `Jam.session_rework`

        Returns:
            str: New session ID
        """
        return await self.session.rework(old_session_key)

    @deprecated("This method is deprecated, use: Jam.otp_code")
    async def get_otp_code(
        self, secret: Union[str, bytes], factor: Optional[int] = None
    ) -> str:
        """Generates an OTP.

        Args:
            secret (str | bytes): User secret key.
            factor (int | None, optional): Unixtime for TOTP(if none, use now time) / Counter for HOTP.

        Deprecated:
            Use: `Jam.otp_code`

        Returns:
            str: OTP code (fixed-length string).
        """
        self._otp_checker()
        return self._otp_module(
            secret=secret, digits=self._otp.digits, digest=self._otp.digest
        ).at(factor)

    @deprecated("This method os deprecated, use: Jam.otp_uri")
    async def get_otp_uri(
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

        Deprecated:
            Use: `Jam.otp_uri`

        Returns:
            str: A string of the form "otpauth://..."
        """
        self._otp_checker()
        return self._otp_module(
            secret=secret, digits=self._otp.digits, digest=self._otp.digest
        ).provisioning_uri(
            name=name, issuer=issuer, type_=self._otp.type, counter=counter
        )

    @deprecated("This method is deprecated, use: Jam.otp_verify_code")
    async def verify_otp_code(
        self,
        secret: Union[str, bytes],
        code: str,
        factor: Optional[int] = None,
        look_ahead: Optional[int] = 1,
    ) -> bool:
        """Checks the OTP code, taking into account the acceptable window.

        Args:
            secret (str | bytes): User secret key.
            code (str): The code entered.
            factor (int | None, optional): Unixtime for TOTP(if none, use now time) / Counter for HOTP.
            look_ahead (int, optional): Acceptable deviation in intervals (±window(totp) / ±look ahead(hotp)). Default is 1.

        Deprecated:
            Use: `Jam.otp_verify_code`

        Returns:
            bool: True if the code matches, otherwise False.
        """
        self._otp_checker()
        return self._otp_module(
            secret=secret, digits=self._otp.digits, digest=self._otp.digest
        ).verify(code=code, factor=factor, look_ahead=look_ahead)

    async def oauth2_get_authorized_url(
        self, provider: str, scope: list[str], **extra_params: Any
    ) -> str:
        """Generate full OAuth2 authorization URL.

        Args:
            provider (str): Provider name
            scope (list[str]): Auth scope
            extra_params (Any): Extra ath params

        Returns:
            str: Authorization url
        """
        return await self.oauth2.get_authorization_url(
            provider, scope, **extra_params
        )

    async def oauth2_fetch_token(
        self,
        provider: str,
        code: str,
        grant_type: str = "authorization_code",
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Exchange authorization code for access token.

        Args:
            provider (str): Provider name
            code (str): OAuth2 code
            grant_type (str): Type of oauth2 grant
            extra_params (Any): Extra auth params if needed

        Returns:
            dict: OAuth2 token
        """
        return await self.oauth2.fetch_token(
            provider, code, grant_type, **extra_params
        )

    async def oauth2_refresh_token(
        self,
        provider: str,
        refresh_token: str,
        grant_type: str = "refresh_token",
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Use refresh token to obtain a new access token.

        Args:
            provider (str): Provider name
            refresh_token (str): Refresh token
            grant_type (str): Grant type
            extra_params (Any): Extra auth params if needed

        Returns:
            dict: Refresh token
        """
        return await self.oauth2.refresh_token(
            provider, refresh_token, grant_type, **extra_params
        )

    async def oauth2_client_credentials_flow(
        self,
        provider: str,
        scope: Optional[list[str]] = None,
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Obtain access token using client credentials flow (no user interaction).

        Args:
            provider (str): Provider name
            scope (list[str] | None): Auth scope
            extra_params (Any): Extra auth params if needed

        Returns:
            dict: JSON with access token
        """
        return await self.oauth2.client_credentials_flow(
            provider, scope, **extra_params
        )
