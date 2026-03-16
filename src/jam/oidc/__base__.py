# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any


class BaseOpenIDConnect(ABC):
    """Base Open ID Conecct."""

    @abstractmethod
    def get_authorization_url(self, state: list[str], scope: str) -> str:
        """Returns the authorization URL for the OpenID Connect flow.

        Args:
            state: The state to include in the authorization URL.
            scope: The scope to include in the authorization URL.

        Returns:
            str: The authorization URL.
        """
        raise NotImplementedError

    @abstractmethod
    def fetch_token(self, code: str, redirect_url: str) -> dict[str, Any]:
        """Returns the access token for the OpenID Connect flow.

        Args:
            code: The authorization code to exchange for a token.
            redirect_url: The redirect URL to use for the token exchange.

        Returns:
            dict[str, Any]: The access token.
        """
        raise NotImplementedError

    @abstractmethod
    def validate_id_token(self, id_token: str) -> dict[str, Any]:
        """Returns the claims for the OpenID Connect flow.

        Args:
            id_token: The ID token to validate.

        Returns:
            dict[str, Any]: The claims for the ID token.
        """
        raise NotImplementedError

    @abstractmethod
    def get_userinfo(self, access_token: str) -> dict[str, Any]:
        """Returns the user info for the OpenID Connect flow.

        Args:
            access_token: The access token to use for the user info request.

        Returns:
            dict[str, Any]: The user info.
        """
        raise NotImplementedError

    @abstractmethod
    def refresh_token(self, refresh_token: str) -> dict[str, Any]:
        """Returns the refreshed token for the OpenID Connect flow.

        Args:
            refresh_token: The refresh token to use for the token refresh.

        Returns:
            dict[str, Any]: The refreshed token.
        """
        raise NotImplementedError
