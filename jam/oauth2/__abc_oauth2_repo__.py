# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from collections.abc import Callable
from secrets import token_urlsafe
from typing import Any, Optional


class BaseOAuth2Client(ABC):
    """Base OAuth2 client instance."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        auth_url: str,
        token_url: str,
        redirect_url: str,
    ) -> None:
        """Constructor.

        Args:
            client_id (str): ID or your client
            client_secret (str): Secret key for your application
            auth_url (str): App auth url
            token_url (str): App token url
            redirect_url (str): Your app url
        """
        self.client_id = client_id
        self._client_secret = client_secret
        self.auth_url = auth_url
        self.token_url = token_url
        self.redirect_url = redirect_url

    @abstractmethod
    def get_authorization_url(self, scope: list[str]) -> str:
        """Get OAuth2 url.

        Args:
            scope (list[str]): Auth scope

        Returns:
            str: URL for auth
        """
        raise NotImplementedError

    @abstractmethod
    def fetch_token(self, code: str) -> str:
        """Exchange code for access token.

        Args:
            code (str): Auth code

        Returns:
            str: Access token
        """
        raise NotImplementedError

    @abstractmethod
    def refresh_token(self, refresh_token: str) -> str:
        """Update access token.

        Args:
            refresh_token (str): Refresh token

        Returns:
            str: New access token
        """
        raise NotImplementedError

    @abstractmethod
    def client_credentials_flow(
        self, scope: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """Obtain access token using client credentials flow (no user interaction).

        Args:
            scope (Optional[list[str]]): Auth scope

        Returns:
            dict: JSON with access token
        """
        raise NotImplementedError


class __BaseOAuth2Server(ABC):
    """Base OAuth2 server instance."""

    def __init__(
        self,
        app_url: str,
        code_factory: Callable[[], str] = lambda: token_urlsafe(8),
    ) -> None:
        """Constructor.

        Args:
            app_url (str): URL of your app
            code_factory (Callable[[] ,str]): Factory for code generation
        """
        self.app_url = app_url
        self.code_factory = code_factory
        raise NotImplementedError("Not implemented in the current version!")

    @property
    def code(self) -> str:
        return self.code_factory()

    ...
