# -*- coding: utf-8 -*-

from jam.oauth2.client import OAuth2Client


class GoogleOAuth2Client(OAuth2Client):
    """Ready to use Google OAuth2 provider.

    See: https://developers.google.com/identity/protocols/oauth2
    """

    def __init__(
        self, client_id: str, client_secret: str, redirect_url: str
    ) -> None:
        """Constructor.

        Args:
            client_id (str): Client ID
            client_secret (str): Secret key
            redirect_url (str): URL for your app
        """
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            redirect_url=redirect_url,
            auth_url="https://accounts.google.com/o/oauth2/v2/auth",
            token_url="",
        )
