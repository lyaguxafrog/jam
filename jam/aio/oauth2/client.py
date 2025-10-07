# -*- coding: utf-8 -*-

import json
import urllib.parse
from contextlib import asynccontextmanager
from http.client import HTTPSConnection
from typing import Any, Optional

from jam.oauth2.__abc_oauth2_repo__ import BaseOAuth2Client


class OAuth2Client(BaseOAuth2Client):
    """Async OAuth2 client."""

    @asynccontextmanager
    async def __http(self, url: str):
        """Create HTTPS connection context manager."""
        parsed = urllib.parse.urlparse(url)
        connection = HTTPSConnection(parsed.netloc)
        try:
            yield connection, parsed
        finally:
            connection.close()

    async def __post_form(
        self, url: str, params: dict[str, Any]
    ) -> dict[str, Any]:
        """Send POST form and parse JSON response."""
        encoded = urllib.parse.urlencode(params)

        async with self.__http(url) as (conn, parsed):
            conn.request(
                "POST",
                parsed.path,
                body=encoded,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response = conn.getresponse()
            raw = response.read().decode("utf-8")

        if not raw:
            raise ValueError("Empty response from token endpoint")

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {k: v[0] for k, v in urllib.parse.parse_qs(raw).items()}

        if response.status >= 400:
            raise RuntimeError(f"OAuth2 error ({response.status}): {data}")

        return data

    async def get_authorization_url(
        self, scope: list[str], **extra_params: Any
    ) -> str:
        """Generate full OAuth2 authorization URL.

        Args:
            scope (list[str]): Auth scope
            extra_params (Any): Extra ath params

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
        self, scope: Optional[list[str]] = None, **extra_params: Any
    ) -> dict[str, Any]:
        """Obtain access token using client credentials flow (no user interaction).

        Args:
            scope (list[str] | None): Auth scope
            extra_params (Any): Extra auth params if needed

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
