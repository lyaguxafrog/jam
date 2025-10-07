# -*- coding: utf-8 -*-

from jam.aio.oauth2.client import OAuth2Client


class YandexOAuth2Client(OAuth2Client):
    """Ready to use yandex oauth2 client.

    See: https://yandex.ru/dev/id/doc
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_url: str,
    ) -> None:
        """Constructor.

        Args:
            client_id (str): Client ID
            client_secret (str): Secret key
            redirect_url (str): Your app URL
        """
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            auth_url="https://oauth.yandex.ru/authorize",
            token_url="https://oauth.yandex.ru/token",
            redirect_url=redirect_url,
        )
