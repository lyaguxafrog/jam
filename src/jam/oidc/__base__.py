# -*- coding: utf-8 -*-

from abc import abstractmethod
from typing import Any

from jam.oauth2.__base__ import BaseOAuth2Client


class BaseOpenIDConnectClient(BaseOAuth2Client):
    """Base OIDC Client."""

    @abstractmethod
    def get_userinfo(self, access_token: str) -> dict[str, Any]:
        """Returns the user info for the OpenID Connect flow.

        Args:
            access_token (str): The access token to use for the user info request.

        Returns:
            dict[str, Any]: The user info.
        """
        raise NotImplementedError

    @abstractmethod
    def validate_id_token(self, id_token: str) -> dict[str, Any]:
        """Returns the claims for the OpenID Connect flow.

        Args:
            id_token (str): The ID token to validate.

        Returns:
            dict[str, Any]: The claims for the ID token.
        """
        raise NotImplementedError
