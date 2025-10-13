# -*- coding: utf-8 -*-

from jam.oauth2.client import OAuth2Client


class GitLabOAuth2Client(OAuth2Client):
    """Ready to use GitLab OAuth2 provider.

    See: https://docs.gitlab.com/api/oauth2/
    """

    def __init__(
        self, client_id: str, client_secret: str, redirect_url: str
    ) -> None:
        """Constructor.

        Args:
            client_id (str): Client ID
            client_secret (str): Secret key
            redirect_url (str): Your app url
        """
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            auth_url="https://gitlab.com/oauth/authorize",
            token_url="https://gitlab.com/oauth/token",
            redirect_url=redirect_url,
        )
