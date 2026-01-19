# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import gc
from typing import Any, Literal, Optional, Union

from jam.encoders import BaseEncoder, JsonEncoder
from jam.jwt.__base__ import BaseJWT
from jam.logger import BaseLogger, JamLogger
from jam.oauth2.__base__ import BaseOAuth2Client
from jam.sessions.__base__ import BaseSessionModule
from jam.utils.config_maker import __config_maker__, __module_loader__


class BaseJam(ABC):
    """Base jam instance."""

    MODULES: dict[str, str] = {}

    def __init__(
        self,
        config: Union[str, dict[str, Any]] = "pyproject.toml",
        pointer: str = "jam",
        *,
        logger: type(BaseLogger) = JamLogger,
        log_level: Literal[
            "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
        ] = "INFO",
        serializer: Union[BaseEncoder, type[BaseEncoder]] = JsonEncoder,
    ) -> None:
        """Initialize instance.

        Args:
                config (Union[str, dict[str, Any]]): Configuration
                pointer (str): Pointer
                logger (BaseLogger): Logger
                log_level (Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]): Log level
                serializer (Union[BaseEncoder, type[BaseBrowser]]): Serializer

        Returns:
                None
        """
        config = __config_maker__(config, pointer)
        main_config = self.__build_main_config(
            config, logger, log_level, serializer
        )

        logger = main_config["logger"]
        log_level = main_config["log_level"]
        serializer = main_config["serializer"]

        self.__logger = logger(log_level)
        self._serializer = serializer
        self.jwt: Optional[BaseJWT] = None
        self.session: Optional[BaseSessionModule] = None
        self.oauth2: Optional[BaseOAuth2Client] = None

        self.__logger.debug(
            f"Initializing BaseJam with log_level={log_level}, serializer={serializer}"
        )
        self.__build_instance(config)
        self.__logger.debug(
            f"BaseJam initialization complete. Modules loaded: jwt={self.jwt is not None}, session={self.session is not None}, oauth2={self.oauth2 is not None}"
        )
        gc.collect()

    def __build_main_config(
        self,
        config: dict[str, Any],
        default_logger: type[BaseLogger],
        default_log_level: Literal[
            "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
        ],
        default_serializer: Union[BaseEncoder, type[BaseEncoder]],
    ) -> dict[str, Any]:
        """Build main params from config like logger, loglevel, etc.

        Args:
            config (dict[str, Any]): Configuration dictionary
            default_logger (type[BaseLogger]): Default logger class
            default_log_level (Literal): Default log level
            default_serializer (Union[BaseEncoder, type[BaseEncoder]]): Default serializer

        Returns:
            dict[str, Any]: Dictionary with logger, log_level, and serializer
        """
        logger = default_logger
        log_level = default_log_level
        serializer = default_serializer

        # Read logger from config
        if "logger" in config:
            logger_cfg = config["logger"]
            if isinstance(logger_cfg, str):
                logger = __module_loader__(logger_cfg)
            elif isinstance(logger_cfg, type) and issubclass(
                logger_cfg, BaseLogger
            ):
                logger = logger_cfg

        if "log_level" in config:
            log_level_cfg = config["log_level"]
            if isinstance(log_level_cfg, str) and log_level_cfg.upper() in (
                "DEBUG",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL",
            ):
                log_level = log_level_cfg.upper()

        if "serializer" in config:
            serializer_cfg = config["serializer"]
            if isinstance(serializer_cfg, str):
                serializer = __module_loader__(serializer_cfg)
            elif isinstance(serializer_cfg, type) and issubclass(
                serializer_cfg, BaseEncoder
            ):
                serializer = serializer_cfg
            elif isinstance(serializer_cfg, BaseEncoder):
                serializer = serializer_cfg

        return {
            "logger": logger,
            "log_level": log_level,
            "serializer": serializer,
        }

    def __build_instance(self, config: dict[str, Any]) -> None:
        """Build instance.

        Load modules from configuration and initialize them.

        Args:
            config (dict[str, Any]): Configuration

        Returns:
            None
        """
        for name, path in self.MODULES.items():
            if name not in config:
                self.__logger.debug(f"Missing configuration for module {name}")
                continue

            try:
                module_cls = __module_loader__(path)
                self.__logger.debug(f"Loading module {name} from {path}")
                params = config.get(name, {})
                self.__logger.debug(
                    f"Module {name} config params: {list(params.keys())}"
                )
                params["logger"] = self.__logger
                params["serializer"] = self._serializer
                module_instance = module_cls(**params)
                self.__setattr__(name, module_instance)
                self.__logger.debug(f"Module {name} initialized successfully")

            except Exception as e:
                self.__logger.error(
                    f"Failed to load module {name} from {path}: {e}",
                    exc_info=True,
                )

    @abstractmethod
    def jwt_make_payload(
        self, exp: Optional[int], data: dict[str, Any]
    ) -> dict[str, Any]:
        """Make JWT-specific payload.

        Args:
            exp (int | None): Token expire, if None -> use default
            data (dict[str, Any]): Data to payload

        Returns:
            dict[str, Any]: Payload
        """
        raise NotImplementedError

    @abstractmethod
    def jwt_create_token(self, payload: dict[str, Any]) -> str:
        """Create JWT token.

        Args:
            payload (dict[str, Any]): Data payload

        Returns:
            str: New token

        Raises:
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None
            EmtpyPrivateKey: If RSA algorithm is selected, but private key None
        """
        raise NotImplementedError

    @abstractmethod
    def jwt_verify_token(
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
        raise NotImplementedError

    @abstractmethod
    def session_create(self, session_key: str, data: dict[str, Any]) -> str:
        """Create new session.

        Args:
            session_key (str): Key for session
            data (dict[str, Any]): Session data

        Returns:
            str: New session ID
        """
        raise NotImplementedError

    @abstractmethod
    def session_get(self, session_id: str) -> Optional[dict[str, Any]]:
        """Get data from session.

        Args:
            session_id (str): Session ID

        Returns:
            dict[str, Any] | None: Session data if exist
        """
        raise NotImplementedError

    @abstractmethod
    def session_delete(self, session_id: str) -> None:
        """Delete session.

        Args:
            session_id (str): Session ID
        """
        raise NotImplementedError

    @abstractmethod
    def session_update(self, session_id: str, data: dict[str, Any]) -> None:
        """Update session data.

        Args:
            session_id (str): Session ID
            data (dict[str, Any]): New data
        """
        raise NotImplementedError

    @abstractmethod
    def session_clear(self, session_key: str) -> None:
        """Delete all sessions by key.

        Args:
            session_key (str): Key of session
        """
        raise NotImplementedError

    @abstractmethod
    def session_rework(self, old_session_id: str) -> str:
        """Rework session.

        Args:
            old_session_id (str): Old session id

        Returns:
            str: New session id
        """
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
    def oauth2_get_authorized_url(
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
        raise NotImplementedError

    @abstractmethod
    def oauth2_fetch_token(
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
        raise NotImplementedError

    @abstractmethod
    def oauth2_refresh_token(
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
        raise NotImplementedError

    @abstractmethod
    def oauth2_client_credentials_flow(
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
        raise NotImplementedError

    @abstractmethod
    def paseto_make_payload(
        self, exp: Optional[int] = None, **data: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate payload for PASETO.

        Args:
            exp (int | None): Custom expire if needed
            data (dict[str, Any]): Data in payload

        Returns:
            dict[str, Any]: New payload
        """
        raise NotImplementedError

    @abstractmethod
    def paseto_create(
        self,
        payload: dict[str, Any],
        footer: Optional[Union[dict[str, Any], str]],
    ) -> str:
        """Create new PASETO.

        Args:
            payload (dict[str, Any]): Payload
            footer (dict[str, Any] | str | None): Payload if needed

        Returns:
            str: PASETO
        """
        raise NotImplementedError

    @abstractmethod
    def paseto_decode(  # mb refactoring this
        self, token: str
    ) -> dict[str, Union[dict, Union[str, dict, None]]]:
        """Decode PASETO and return payload and footer.

        Args:
            token (str): PASETO

        Returns:
            dict: {`payload`: PAYLOAD, `footer`: FOOTER}
        """
        raise NotImplementedError
