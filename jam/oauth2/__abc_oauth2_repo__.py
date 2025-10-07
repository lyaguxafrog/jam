# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


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
        self.__client_secret = client_secret
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
