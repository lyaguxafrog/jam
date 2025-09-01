# -*- coding: utf-8 -*-

import datetime
from collections.abc import Callable
from typing import Any, Literal, Optional, Union
from uuid import uuid4

from jam.__logger__ import logger
from jam.exceptions import TokenInBlackList, TokenNotInWhiteList
from jam.jwt.lists.json import JSONList
from jam.jwt.lists.redis import RedisList
from jam.jwt.tools import __gen_jwt__, __validate_jwt__
from jam.utils.config_maker import __module_loader__


class BaseModule:
    """The base module from which all other modules inherit."""

    def __init__(
        self,
        module_type: str = "custom",
    ) -> None:
        """Class constructor.

        Args:
            module_type (str): Type of module
        """
        self._type = module_type


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

    def make_payload(self, exp: int | None = None, **data) -> dict[str, Any]:
        """Payload maker tool.

        Args:
            exp (int | None): If none exp = JWTModule.exp
            **data: Custom data
        """
        if not exp:
            logger.debug("Set expire from default")
            _exp = self.exp
        else:
            _exp = exp
        payload = {
            "jti": str(uuid4()),
            "exp": _exp + datetime.datetime.now().timestamp(),
            "iat": datetime.datetime.now().timestamp(),
        }
        payload.update(**data)
        logger.debug(f"Gen payload: {payload}")
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

        logger.debug(f"Gen jwt token: {token}")
        logger.debug(f"Token header: {header}")
        logger.debug(f"Token payload: {payload}")

        if self.list:  # type: ignore
            if self.list.__list_type__ == "white":
                logger.debug("Add JWT token to white list")
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
                    logger.debug("Token in white list")
                    pass
            if self.list.__list_type__ == "black":  # type: ignore
                if self.list.check(token):  # type: ignore
                    raise TokenInBlackList
                else:
                    logger.debug("Token not in black list")
                    pass

        payload = __validate_jwt__(
            token=token,
            check_exp=check_exp,
            secret=self._secret_key,
            public_key=self.public_key,
        )

        return payload


class SessionModule(BaseModule):
    """Module for session management."""

    def __init__(
        self,
        sessions_type: Literal["redis", "json", "custom"],
        id_factory: Callable[[], str] = lambda: str(uuid4()),
        is_session_crypt: bool = False,
        session_aes_secret: Optional[bytes] = None,
        **module_kwargs: Any,
    ) -> None:
        """Class constructor.

        Args:
            sessions_type (Literal["redis", "json"]): Type of session storage.
            id_factory (Callable[[], str], optional): A callable that generates unique IDs. Defaults to a UUID factory.
            is_session_crypt (bool, optional): If True, session keys will be encoded. Defaults to False.
            session_aes_secret (Optional[bytes], optional): AES secret for encoding session keys.
            **module_kwargs (Any): Additional keyword arguments for the session module. See <DOCS>
        """
        super().__init__(module_type="session")
        from jam.sessions.__abc_session_repo__ import BaseSessionModule

        self.module: BaseSessionModule

        if sessions_type == "redis":
            from jam.sessions.redis import RedisSessions

            self.module = RedisSessions(
                redis_uri=module_kwargs.get(
                    "redis_uri", "redis://localhost:6379/0"
                ),
                redis_sessions_key=module_kwargs.get(
                    "sessions_path", "sessions"
                ),
                default_ttl=module_kwargs.get("session_ttl"),
                is_session_crypt=is_session_crypt,
                session_aes_secret=session_aes_secret,
                id_factory=id_factory,
            )
        elif sessions_type == "json":
            from jam.sessions.json import JSONSessions

            self.module = JSONSessions(
                json_path=module_kwargs.get("json_path", "sessions.json"),
                is_session_crypt=is_session_crypt,
                session_aes_secret=session_aes_secret,
                id_factory=id_factory,
            )
        elif sessions_type == "custom":
            _module: Optional[Union[Callable, str]] = module_kwargs.get(
                "custom_module"
            )
            if not _module:
                raise ValueError("Custom module not provided")
            module_kwargs.__delitem__("custom_module")
            if isinstance(_module, str):
                _m = __module_loader__(_module)
                self.module = _m(
                    is_session_crypt=is_session_crypt,
                    session_aes_secret=session_aes_secret,
                    id_factory=id_factory,
                    **module_kwargs,
                )
                del _m
            elif callable(_module):
                self.module = _module(
                    is_session_crypt=is_session_crypt,
                    session_aes_secret=session_aes_secret,
                    id_factory=id_factory,
                    **module_kwargs,
                )
            del _module
            if not self.module:
                raise ValueError("Custom module not provided")
            if not isinstance(self.module, BaseSessionModule):
                raise TypeError(
                    "Custom module must be an instance of BaseSessionModule. See <DOCS>"
                )
        else:
            raise ValueError(
                f"Unsupported session type: {sessions_type} \n"
                f"See docs: https://jam.makridenko.ru/sessions/"
            )

    def create(self, session_key: str, data: dict) -> str:
        """Create a new session with the given session key and data.

        Args:
            session_key (str): The key for the session.
            data (dict): The data to be stored in the session.

        Returns:
            str: The ID of the created session.
        """
        return self.module.create(session_key, data)

    def get(self, session_id: str) -> Optional[dict]:
        """Retrieve a session by its key or ID.

        Args:
            session_id (str): The ID of the session to retrieve.

        Returns:
            dict | None: The data stored in the session.

        Raises:
            SessionNotFoundError: If the session does not exist.
        """
        return self.module.get(session_id)

    def rework(self, session_id: str) -> str:
        """Reworks a session and returns its new ID.

        Args:
            session_id (str): The ID of the session to rework.

        Returns:
            str: The new ID of the reworked session.

        Raises:
            SessionNotFoundError: If the session does not exist.
        """
        return self.module.rework(session_id)

    def delete(self, session_id: str) -> None:
        """Delete a session by its key or ID.

        Args:
            session_id (str): The ID of the session to delete.

        Raises:
            SessionNotFoundError: If the session does not exist.
        """
        self.module.delete(session_id)

    def update(self, session_id: str, data: dict) -> None:
        """Update an existing session with new data.

        Args:
            session_id (str): The ID of the session to update.
            data (dict): The new data to be stored in the session.

        Raises:
            SessionNotFoundError: If the session does not exist.
        """
        self.module.update(session_id, data)

    def clear(self, session_key: str) -> None:
        """Clear all sessions by key.

        Args:
            session_key (str): The session key to clear.

        Raises:
            SessionNotFoundError: If the session does not exist.
        """
        self.module.clear(session_key)
