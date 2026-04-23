# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import gc
from typing import Any, Literal

from jam.encoders import BaseEncoder, JsonEncoder
from jam.exceptions import JamConfigurationError
from jam.jose.__base__ import BaseJWE, BaseJWS, BaseJWT
from jam.logger import BaseLogger, JamLogger
from jam.oauth2.__base__ import BaseOAuth2Client
from jam.otp.__base__ import BaseOTP, OTPConfig
from jam.paseto.__base__ import BasePASETO
from jam.sessions.__base__ import BaseSessionModule
from jam.utils.config_maker import __config_maker__, __module_loader__


class BaseJam(ABC):
    """Base jam instance."""

    MODULES: dict[str, str | dict[str, str]] = {}

    def __init__(
        self,
        config: str | dict[str, Any] = "pyproject.toml",
        pointer: str = "jam",
        *,
        logger: type[BaseLogger] = JamLogger,
        log_level: Literal[
            "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
        ] = "INFO",
        serializer: BaseEncoder | type[BaseEncoder] = JsonEncoder,
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

        self._logger = logger(log_level)
        self._serializer = serializer
        self.jwt: BaseJWT | None = None
        self.jws: BaseJWS | None = None
        self.jwe: BaseJWE | None = None
        self.jose: dict[str, Any] | None = None
        self.session: BaseSessionModule | None = None
        self.oauth2: dict[str, BaseOAuth2Client] | None = None
        self.otp: OTPConfig | None = None
        self.paseto: BasePASETO | None = None

        self._logger.debug(
            f"Initializing BaseJam with log_level={log_level}, serializer={serializer}"
        )
        self.__build_instance(config)
        self._otp: type[BaseOTP] | None = self.__otp(
            self.otp.type if self.otp else None
        )
        self._logger.debug(
            "BaseJam initialization complete. Modules loaded:\n"
            f" jwt={self.jwt is not None}, jose={self.jose is not None}, session={self.session is not None}, oauth2={self.oauth2 is not None}"
        )
        gc.collect()

    def __build_main_config(
        self,
        config: dict[str, Any],
        default_logger: type[BaseLogger],
        default_log_level: Literal[
            "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
        ],
        default_serializer: BaseEncoder | type[BaseEncoder],
    ) -> dict[str, Any]:
        """Build main params from config like logger, loglevel, etc.

        Args:
            config (dict[str, Any]): Configuration dictionary
            default_logger (type[BaseLogger]): Default logger class
            default_log_level (Literal): Default log level
            default_serializer (BaseEncoder | type[BaseEncoder]): Default serializer

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
        Supports both flat modules (name -> path) and nested modules (name -> {subname -> path}).

        Args:
            config (dict[str, Any]): Configuration

        Returns:
            None
        """
        for name, path in self.MODULES.items():
            if name not in config:
                self._logger.debug(f"Missing configuration for module {name}")
                continue

            if isinstance(path, dict):
                subconfig = config.get(name, {})
                if not isinstance(subconfig, dict):
                    subconfig = {}

                for subname, subpath in path.items():
                    if subname not in subconfig:
                        self._logger.debug(
                            f"Missing configuration for module {name}.{subname}"
                        )
                        continue

                    try:
                        module_cls = __module_loader__(subpath)
                        self._logger.debug(
                            f"Loading module {name}.{subname} from {subpath}"
                        )
                        params = subconfig.get(subname, {})
                        self._logger.debug(
                            f"Module {name}.{subname} config params: {list(params.keys())}"
                        )
                        module_instance = module_cls(**params)

                        if self.jose is None:
                            self.jose = {}
                        self.jose[subname] = module_instance

                        if subname == "jwt":
                            self.jwt = module_instance
                        elif subname == "jws":
                            self.jws = module_instance
                        elif subname == "jwe":
                            self.jwe = module_instance

                        self._logger.debug(
                            f"Module {name}.{subname} initialized successfully"
                        )

                    except Exception as e:
                        self._logger.error(
                            f"Failed to load module {name}.{subname} from {subpath}: {e}",
                            exc_info=True,
                        )
            else:
                try:
                    module_cls = __module_loader__(path)
                    self._logger.debug(f"Loading module {name} from {path}")
                    params = config.get(name, {})
                    self._logger.debug(
                        f"Module {name} config params: {list(params.keys())}"
                    )
                    module_instance = module_cls(**params)
                    self.__setattr__(name, module_instance)
                    self._logger.debug(
                        f"Module {name} initialized successfully"
                    )

                except Exception as e:
                    self._logger.error(
                        f"Failed to load module {name} from {path}: {e}",
                        exc_info=True,
                    )

    def __otp(
        self, type: Literal["totp", "hotp"] | None = None
    ) -> type[BaseOTP] | None:
        """Get OTP type."""
        match type:
            case "hotp":
                from jam.otp.hotp import HOTP

                return HOTP
            case "totp":
                from jam.otp.totp import TOTP

                return TOTP
            case None:
                return None
            case _:
                raise JamConfigurationError(message="Unknown OTP type.")

    @abstractmethod
    def jwt_encode(
        self,
        iss: str | None = None,
        sub: str | None = None,
        aud: str | None = None,
        exp: int | None = None,
        nbf: int | None = None,
        *,
        payload: dict[str, Any] | None = None,
        header: dict[str, Any] | None = None,
    ) -> str:
        """Encode the JWT with the given expire, header, and payload.

        Args:
            exp (int | None): The expiration time in seconds.
            nbf (int | None): The not-before time in seconds.
            iss (str | None): The issuer.
            sub (str | None): The subject.
            aud (str | None): The audience.
            header (dict[str, Any] | None): The header to include in the JWT.
            payload (dict[str, Any] | None): The payload to include in the JWT.

        Returns:
            str: The encoded JWT.
        """
        raise NotImplementedError

    @abstractmethod
    def jwt_decode(
        self,
        token: str,
        check_exp: bool = True,
        check_list: bool = True,
        check_nbf: bool = False,
        include_headers: bool = False,
    ) -> dict[str, Any]:
        """Verify and decode JWT token.

        Args:
            token (str): JWT token
            check_exp (bool): Check expire
            check_list (bool): Check white/black list. Docs: https://jam.makridenko.ru/jwt/lists/what/
            check_nbf (bool): Check not-before time
            include_headers (bool): Include headers in the decoded payload

        Returns:
            dict[str, Any]: Decoded payload

        """
        raise NotImplementedError

    @abstractmethod
    def jws_sign(
        self,
        data: dict[str, Any] | str,
        header: dict[str, Any] | None = None,
    ) -> str:
        """Sign data using JWS.

        Args:
            data: Data to sign. If dict, will be JSON encoded.
            header: JWS header.

        Returns:
            str: JWS token.
        """
        raise NotImplementedError

    @abstractmethod
    def jws_verify(self, token: str) -> dict[str, Any]:
        """Verify JWS token.

        Args:
            token: JWS token.

        Returns:
            dict[str, Any]: Decoded payload.

        Raises:
            JamJWSVerificationError: If verification fails.
        """
        raise NotImplementedError

    @abstractmethod
    def jwe_encrypt(
        self,
        data: dict[str, Any] | str,
        header: dict[str, Any] | None = None,
    ) -> str:
        """Encrypt data using JWE.

        Args:
            data: Data to encrypt. If dict, will be JSON encoded.
            header: JWE header.

        Returns:
            str: JWE token.
        """
        raise NotImplementedError

    @abstractmethod
    def jwe_decrypt(self, token: str) -> bytes:
        """Decrypt JWE token.

        Args:
            token: JWE token.

        Returns:
            bytes: Decrypted data.

        Raises:
            JamJWEDecryptionError: If decryption fails.
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
    def session_get(self, session_id: str) -> dict[str, Any] | None:
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
    def otp_code(self, secret: str | bytes, factor: int | None = None) -> str:
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
        name: str,
        issuer: str,
        counter: int | None = None,
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
        secret: str | bytes,
        code: str,
        factor: int | None = None,
        look_ahead: int | None = 1,
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
        scope: list[str] | None = None,
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
        self, exp: int | None = None, **data: dict[str, Any]
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
        footer: dict[str, Any] | str | None,
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
    def paseto_decode(
        self, token: str
    ) -> dict[str, dict[str, Any] | str | None]:
        """Decode PASETO and return payload and footer.

        Args:
            token (str): PASETO

        Returns:
            dict: {"payload": PAYLOAD, "footer": FOOTER}
        """
        raise NotImplementedError
