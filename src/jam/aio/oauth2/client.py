# -*- coding: utf-8 -*-

import asyncio
from contextlib import contextmanager
from http.client import HTTPSConnection
import json
from typing import Any
import urllib.parse

from jam.oauth2.__base__ import BaseOAuth2Client
from jam.exceptions import JamOAuth2Error, JamOAuth2EmptyRaw


class OAuth2Client(BaseOAuth2Client):
    """Async universal OAuth2 client implementation."""

    @contextmanager
    def __http(self, url: str):
        """Create HTTPS connection context manager."""
        parsed = urllib.parse.urlparse(url)
        connection = HTTPSConnection(parsed.netloc)
        try:
            yield connection, parsed
        finally:
            connection.close()

    def get_authorization_url(
        self, scope: list[str], **extra_params: Any
    ) -> str:
        """Generate full OAuth2 authorization URL.

        Args:
            scope (list[str]): Auth scope
            extra_params (Any): Extra auth params

        Returns:
            str: Authorization url
        """
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_url,
            "response_type": "code",
            "scope": " ".join(scope),
        }
        params.update(
            extra_params
        )  # for example: access_type='offline', state='xyz'
        return f"{self.auth_url}?{urllib.parse.urlencode(params)}"

    async def fetch_token(
        self,
        code: str,
        grant_type: str = "authorization_code",
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Exchange authorization code for access token.

        Args:
            code (str): OAuth2 code
            grant_type (str): Type of oauth2 grant
            extra_params (Any): Extra auth params if needed

        Returns:
            dict: OAuth2 token
        """
        body = {
            "client_id": self.client_id,
            "client_secret": self._client_secret,
            "code": code,
            "redirect_uri": self.redirect_url,
            "grant_type": grant_type,
        }
        body.update(extra_params)

        return await self.__post_form(self.token_url, body)

    async def refresh_token(
        self,
        refresh_token: str,
        grant_type: str = "refresh_token",
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Use refresh token to obtain a new access token.

        Args:
            refresh_token (str): Refresh token
            grant_type (str): Grant type
            extra_params (Any): Extra auth params if needed

        Returns:
            dict: Refresh token
        """
        body = {
            "client_id": self.client_id,
            "client_secret": self._client_secret,
            "refresh_token": refresh_token,
            "grant_type": grant_type,
        }
        body.update(extra_params)

        return await self.__post_form(self.token_url, body)

    async def client_credentials_flow(
        self, scope: list[str] | None = None, **extra_params: Any
    ) -> dict[str, Any]:
        """Obtain access token using client credentials flow (no user interaction).

        Args:
            scope (list[str] | None): Auth scope
            extra_params (Any): Extra auth params if needed

        Raises:
            JamOAuth2EmptyRaw: If response is empty
            JamOAuth2Error: HTTP error

        Returns:
            dict: JSON with access token
        """
        body = {
            "client_id": self.client_id,
            "client_secret": self._client_secret,
            "grant_type": "client_credentials",
        }
        if scope:
            body["scope"] = " ".join(scope)
        body.update(extra_params)

        return await self.__post_form(self.token_url, body)

    async def __post_form(
        self, url: str, params: dict[str, Any]
    ) -> dict[str, Any]:
        """Send POST form and parse JSON response (async version)."""
        encoded = urllib.parse.urlencode(params)

        def _sync_post():
            """Synchronous POST operation wrapped for async execution."""
            with self.__http(url) as (conn, parsed):
                conn.request(
                    "POST",
                    parsed.path,
                    body=encoded,
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                )
                response = conn.getresponse()
                raw = response.read().decode("utf-8")

            if not raw:
                raise JamOAuth2EmptyRaw(
                    details={
                        "endpoint": url,
                        "methid": "POST",
                        "params": params
                    }
                )

            try:
                data = self._serializer.loads(raw)
            except (json.JSONDecodeError, AttributeError):
                data = {k: v[0] for k, v in urllib.parse.parse_qs(raw).items()}

            if response.status >= 400:
                raise JamOAuth2Error(
                    details={
                        "status": response.status,
                        "reason": response.reason,
                        "data": data
                    }
                )

            return data

        return await asyncio.to_thread(_sync_post)
