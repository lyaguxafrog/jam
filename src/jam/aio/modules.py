# -*- coding: utf-8 -*-

from collections.abc import Callable
from typing import Any, Literal, Optional, Union
from uuid import uuid4

from jam.aio.oauth2.client import OAuth2Client
from jam.exceptions import (
    ProviderNotConfigurError,
)
from jam.modules import BaseModule
from jam.utils.config_maker import __module_loader__


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
            from jam.aio.sessions.redis import RedisSessions

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
            from jam.aio.sessions.json import JSONSessions

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

    async def create(self, session_key: str, data: dict) -> str:
        """Create a new session with the given session key and data.

        Args:
            session_key (str): The key for the session.
            data (dict): The data to be stored in the session.

        Returns:
            str: The ID of the created session.
        """
        return await self.module.create(session_key, data)

    async def get(self, session_id: str) -> Optional[dict]:
        """Retrieve a session by its key or ID.

        Args:
            session_id (str): The ID of the session to retrieve.

        Returns:
            dict | None: The data stored in the session.

        Raises:
            SessionNotFoundError: If the session does not exist.
        """
        return await self.module.get(session_id)

    async def rework(self, session_id: str) -> str:
        """Reworks a session and returns its new ID.

        Args:
            session_id (str): The ID of the session to rework.

        Returns:
            str: The new ID of the reworked session.

        Raises:
            SessionNotFoundError: If the session does not exist.
        """
        return await self.module.rework(session_id)

    async def delete(self, session_id: str) -> None:
        """Delete a session by its key or ID.

        Args:
            session_id (str): The ID of the session to delete.

        Raises:
            SessionNotFoundError: If the session does not exist.
        """
        await self.module.delete(session_id)

    async def update(self, session_id: str, data: dict) -> None:
        """Update an existing session with new data.

        Args:
            session_id (str): The ID of the session to update.
            data (dict): The new data to be stored in the session.

        Raises:
            SessionNotFoundError: If the session does not exist.
        """
        await self.module.update(session_id, data)

    async def clear(self, session_key: str) -> None:
        """Clear all sessions by key.

        Args:
            session_key (str): The session key to clear.

        Raises:
            SessionNotFoundError: If the session does not exist.
        """
        await self.module.clear(session_key)


class OAuth2Module(BaseModule):
    """OAuth2 module."""

    BUILTIN_PROVIDERS = {
        "github": "jam.aio.oauth2.GitHubOAuth2Client",
        "gitlab": "jam.aio.oauth2.GitLabOAuth2Client",
        "google": "jam.aio.oauth2.GoogleOAuth2Client",
        "yandex": "jam.aio.oauth2.YandexOAuth2Client",
    }

    DEFAULT_CLIENT = "jam.aio.oauth2.client.OAuth2Client"

    def __init__(self, config: dict[str, str]) -> None:
        """Constructor.

        Args:
            config (dict[str, str]): Config
        """
        super().__init__(module_type="oauth2")
        self.providers = {}
        providers_cfg = config.get("providers", {})

        self.providers = {
            name: (
                __module_loader__(cfg.pop("module"))(**cfg)
                if "module" in cfg
                else __module_loader__(
                    self.BUILTIN_PROVIDERS.get(name, self.DEFAULT_CLIENT)
                )(**cfg)
            )
            for name, cfg in providers_cfg.items()
        }

    def __provider_getter(self, provider: str) -> OAuth2Client:
        prv_: OAuth2Client = self.providers.get(provider)
        if not prv_:
            raise ProviderNotConfigurError
        else:
            return prv_

    async def get_authorization_url(
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
        prv_ = self.__provider_getter(provider)
        return await prv_.get_authorization_url(scope, **extra_params)

    async def fetch_token(
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
        return await self.__provider_getter(provider).fetch_token(
            code, grant_type, **extra_params
        )

    async def refresh_token(
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
        return await self.__provider_getter(provider).refresh_token(
            refresh_token, grant_type, **extra_params
        )

    async def client_credentials_flow(
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
        return await self.__provider_getter(provider).client_credentials_flow(
            scope, **extra_params
        )
