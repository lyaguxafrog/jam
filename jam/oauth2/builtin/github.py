# -*- coding: utf-8 -*-

from jam.oauth2.client import OAuth2Client


class GitHubOAuth2Client(OAuth2Client):
    """Rady to use GitHub OAuth2 provider.

    See: https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
    """

    def __init__(
        self, client_id: str, client_secret: str, redirect_url: str
    ) -> None:
        """Constructor.

        Args:
            client_id (str): ID of your app
            client_secret (str): Secret key
            redirect_url (str): URL for your app
        """
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            auth_url="https://github.com/login/oauth/authorize",
            token_url="https://github.com/login/oauth/access_token",
            redirect_url=redirect_url,
        )
