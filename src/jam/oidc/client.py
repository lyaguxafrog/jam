# -*- coding: utf-8 -*-

from typing import Any

from jam.oauth2.client import OAuth2Client
from jam.oidc.__base__ import BaseOpenIDConnectClient


class OpenIDConnectClient(BaseOpenIDConnectClient, OAuth2Client):
    """OIDC Client."""

    def get_userinfo(self, access_token: str) -> dict[str, Any]:
        """Returns the user info for the OpenID Connect flow.

        Args:
            access_token (str): The access token to use for the user info request.

        Returns:
            dict[str, Any]: The user info.
        """
        ...
