# -*- coding: utf-8 -*-

import datetime
import json
from typing import Any, Union
import uuid

from jam.aio import Jam as AioJam
from jam.instance import Jam
from jam.jwt.utils import base64url_decode
from jam.tests.fakers import (
    fake_jwt_token,
    fake_oauth2_token,
    fake_paseto_token,
    generate_session_id,
)


class TestJam(Jam):
    """A test client for Jam.

    This client provides fake implementations of all Jam methods for testing purposes.
    All operations always succeed and return fake but valid data.

    Examples:
        ```python
        import pytest
        from jam.tests import TestJam
        from jam.tests.fakers import invalid_token

        @pytest.fixture
        def client() -> TestJam:
            return TestJam()

        def test_jwt_token(client) -> None:
            payload = {"user_id": 1, "role": "admin"}
            token = client.jwt_create_token(payload)
            assert isinstance(token, str)
            assert token.count(".") == 2

            verified_payload = client.jwt_verify_token(token, check_exp=False, check_list=False)
            assert verified_payload == payload

        def test_invalid_jwt_token(client) -> None:
            token = invalid_token()
            with pytest.raises(ValueError):
                client.jwt_verify_token(token, check_exp=False, check_list=False)
        ```
    """

    __test__ = False

    def __init__(
        self,
        config: Union[str, dict[str, Any]] | None = None,
        pointer: str = "jam",
    ) -> None:
        """Class constructor.

        Args:
            config (str | dict[str, Any] | None): Jam configuration.
            pointer (str): Pointer for the client instance.
        """
        super().__init__(config=config or {}, pointer=pointer)
        self.module = self
        self._sessions: dict[str, dict[str, Any]] = {}
        self._session_keys: dict[str, str] = {}

    def jwt_make_payload(
        self, exp: int | None, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Make JWT-specific payload.

        Args:
            exp (int | None): Token expire, if None -> use default
            data (dict[str, Any]): Data to payload

        Returns:
            dict[str, Any]: Payload
        """
        payload = {
            "iat": datetime.datetime.now().timestamp(),
            "exp": (datetime.datetime.now().timestamp() + exp) if exp else None,
            "jti": str(uuid.uuid4()),
        }
        payload = payload | data
        return payload

    def jwt_create_token(self, payload: dict[str, Any]) -> str:
        """Create JWT token.

        Args:
            payload (dict[str, Any]): Data payload

        Returns:
            str: New token
        """
        return fake_jwt_token(payload)

    def jwt_verify_token(
        self, token: str, check_exp: bool = True, check_list: bool = True
    ) -> dict[str, Any]:
        """Verify and decode JWT token.

        Args:
            token (str): JWT token
            check_exp (bool): Check expire
            check_list (bool): Check white/black list

        Returns:
            dict[str, Any]: Decoded payload

        Raises:
            ValueError: If the token format is invalid.
        """
        try:
            headers, payload, _ = token.split(".")
            headers = json.loads(base64url_decode(headers).decode("utf-8"))
            payload = base64url_decode(payload).decode("utf-8")

            if headers.get("typ") == "fake-JWT":
                return json.loads(payload)
            else:
                raise ValueError("Invalid token format.")
        except (ValueError, IndexError, json.JSONDecodeError) as e:
            raise ValueError("Invalid token format.") from e

    def session_create(self, session_key: str, data: dict[str, Any]) -> str:
        """Create new session.

        Args:
            session_key (str): Key for session
            data (dict[str, Any]): Session data

        Returns:
            str: New session ID
        """
        session_id = generate_session_id()
        self._sessions[session_id] = data.copy()
        self._session_keys[session_id] = session_key
        return session_id

    def session_get(self, session_id: str) -> dict[str, Any] | None:
        """Get data from session.

        Args:
            session_id (str): Session ID

        Returns:
            dict[str, Any] | None: Session data if exist
        """
        return self._sessions.get(session_id)

    def session_delete(self, session_id: str) -> None:
        """Delete session.

        Args:
            session_id (str): Session ID
        """
        self._sessions.pop(session_id, None)
        self._session_keys.pop(session_id, None)

    def session_update(self, session_id: str, data: dict[str, Any]) -> None:
        """Update session data.

        Args:
            session_id (str): Session ID
            data (dict[str, Any]): New data
        """
        if session_id in self._sessions:
            self._sessions[session_id].update(data)

    def session_clear(self, session_key: str) -> None:
        """Delete all sessions by key.

        Args:
            session_key (str): Key of session
        """
        to_delete = [
            session_id
            for session_id, key in self._session_keys.items()
            if key == session_key
        ]
        for session_id in to_delete:
            self._sessions.pop(session_id, None)
            self._session_keys.pop(session_id, None)

    def session_rework(self, old_session_id: str) -> str:
        """Rework session.

        Args:
            old_session_id (str): Old session id

        Returns:
            str: New session id
        """
        if old_session_id not in self._sessions:
            session_id = generate_session_id()
            self._sessions[session_id] = {}
            return session_id

        old_data = self._sessions[old_session_id].copy()
        old_key = self._session_keys.get(old_session_id, "default")
        new_session_id = generate_session_id()

        self._sessions[new_session_id] = old_data
        self._session_keys[new_session_id] = old_key

        return new_session_id

    def otp_code(self, secret: str | bytes, factor: int | None = None) -> str:
        """Generates an OTP.

        Args:
            secret (str | bytes): User secret key.
            factor (int | None, optional): Unixtime for TOTP(if none, use now time) / Counter for HOTP.

        Returns:
            str: OTP code (fixed-length string).
        """
        return "123456"

    def otp_uri(
        self,
        secret: str,
        name: str | None = None,
        issuer: str | None = None,
        counter: int | None = None,
    ) -> str:
        """Generates an otpauth:// URI for Google Authenticator.

        Args:
            secret (str): User secret key.
            name (str): Account name (e.g., email).
            issuer (str): Service name (e.g., "GitHub").
            counter (int | None, optional): Counter (for HOTP). Default is None.

        Returns:
            str: A string of the form "otpauth://..."
        """
        uri = f"otpauth://totp/{name or 'user'}?secret={secret}"
        if issuer:
            uri += f"&issuer={issuer}"
        if counter is not None:
            uri += f"&counter={counter}"
        return uri

    def otp_verify_code(
        self,
        secret: str | bytes,
        code: str,
        factor: int | None = None,
        look_ahead: int | None = 1,
    ) -> bool:
        """Checks the OTP code, taking into account the acceptable window.

        Args:
            secret (str | bytes): User secret key.
            code (str): The code entered.
            factor (int | None, optional): Unixtime for TOTP(if none, use now time) / Counter for HOTP.
            look_ahead (int, optional): Acceptable deviation in intervals (±window(totp) / ±look ahead(hotp)). Default is 1.

        Returns:
            bool: True if the code matches, otherwise False.
        """
        return code == "123456"

    def oauth2_get_authorized_url(
        self, provider: str, scope: list[str], **extra_params: Any
    ) -> str:
        """Generate full OAuth2 authorization URL.

        Args:
            provider (str): Provider name
            scope (list[str]): Auth scope
            extra_params (Any): Extra auth params

        Returns:
            str: Authorization url
        """
        return f"https://{provider}/auth&client_id=TEST_CLIENT&redirect_uri=https%3A%2F%2Fexample.com&response_type=code"

    def oauth2_fetch_token(
        self,
        provider: str,
        code: str,
        grant_type: str = "authorization_code",
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Exchange authorization code for access token.

        Args:
            provider (str): Provider name
            code (str): OAuth2 code
            grant_type (str): Type of oauth2 grant
            extra_params (Any): Extra auth params if needed

        Returns:
            dict: OAuth2 token
        """
        return {
            "access_token": fake_oauth2_token(),
            "access_expire": 9999999,
            "refresh_token": fake_oauth2_token(),
            "refresh_expire": 999999,
            "token_type": "bearer",
        }

    def oauth2_refresh_token(
        self,
        provider: str,
        refresh_token: str,
        grant_type: str = "refresh_token",
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Use refresh token to obtain a new access token.

        Args:
            provider (str): Provider name
            refresh_token (str): Refresh token
            grant_type (str): Grant type
            extra_params (Any): Extra auth params if needed

        Returns:
            dict: Refresh token
        """
        return {
            "access_token": fake_oauth2_token(),
            "access_expire": 9999999,
            "refresh_token": fake_oauth2_token(),
            "refresh_expire": 999999,
            "token_type": "bearer",
        }

    def oauth2_client_credentials_flow(
        self,
        provider: str,
        scope: list[str] | None = None,
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Obtain access token using client credentials flow (no user interaction).

        Args:
            provider (str): OAuth2 provider
            scope (list[str] | None): Auth scope
            extra_params (Any): Extra auth params if needed

        Returns:
            dict: JSON with access token
        """
        return {
            "access_token": fake_oauth2_token(),
            "access_expire": 9999999,
            "refresh_token": fake_oauth2_token(),
            "refresh_expire": 999999,
            "token_type": "bearer",
        }

    def paseto_make_payload(
        self, exp: int | None = None, **data: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate payload for PASETO.

        Args:
            exp (int | None): Custom expire if needed
            data (dict[str, Any]): Data in payload

        Returns:
            dict[str, Any]: New payload
        """
        from jam.paseto.utils import payload_maker

        return payload_maker(expire=exp, data=data)

    def paseto_create(
        self,
        payload: dict[str, Any],
        footer: dict[str, Any] | str | None,
    ) -> str:
        """Create new PASETO.

        Args:
            payload (dict[str, Any]): Payload
            footer (dict | str  | None): Footer

        Returns:
            str: New token
        """
        return fake_paseto_token(payload, footer)

    def paseto_decode(
        self, token: str, check_exp: bool = True, check_list: bool = True
    ) -> dict[str, dict[str, Any] | str | None]:
        """Decode PASETO.

        Args:
            token (str): Token
            check_exp (bool): Check exp in payload
            check_list (bool): Check token in list

        Returns:
            dict: {'payload' PAYLOAD, 'footer': FOOTER}
        """
        try:
            parts = token.split(".")
            if len(parts) < 3:
                raise ValueError("Invalid PASETO token format")

            if parts[0] not in ("v1", "v2", "v3", "v4"):
                raise ValueError("Invalid PASETO version")

            payload_part = parts[2]
            footer_part = parts[3] if len(parts) > 3 else None

            payload = json.loads(base64url_decode(payload_part).decode("utf-8"))

            footer = None
            if footer_part:
                try:
                    footer = json.loads(
                        base64url_decode(footer_part).decode("utf-8")
                    )
                except (json.JSONDecodeError, UnicodeDecodeError):
                    footer = base64url_decode(footer_part).decode("utf-8")

            return {"payload": payload, "footer": footer}
        except (
            ValueError,
            IndexError,
            json.JSONDecodeError,
            UnicodeDecodeError,
        ) as e:
            raise ValueError("Invalid PASETO token format.") from e


class TestAsyncJam(AioJam):
    """A test async client for Jam.

    This client provides fake async implementations of all Jam methods for testing purposes.
    All operations always succeed and return fake but valid data.

    Example:
        ```python
        import pytest
        import pytest_asyncio
        from jam.tests import TestAsyncJam
        from jam.tests.fakers import invalid_token

        @pytest_asyncio.fixture
        async def client() -> TestAsyncJam:
            return TestAsyncJam()

        @pytest.mark.asyncio
        async def test_jwt_token(client) -> None:
            payload = {"user_id": 1, "role": "admin"}
            token = await client.jwt_create_token(payload)
            assert isinstance(token, str)
            assert token.count(".") == 2

            verified_payload = await client.jwt_verify_token(token, check_exp=False, check_list=False)
            assert verified_payload == payload
        ```
    """

    __test__ = False

    def __init__(
        self,
        config: Union[str, dict[str, Any]] | None = None,
        pointer: str = "jam",
    ) -> None:
        """Class constructor.

        Args:
            config (str | dict[str, Any] | None): Jam configuration.
            pointer (str): Pointer for the client instance.
        """
        super().__init__(config=config or {}, pointer=pointer)
        self.module = self
        self._sessions: dict[str, dict[str, Any]] = {}
        self._session_keys: dict[str, str] = {}

    async def jwt_make_payload(
        self, exp: int | None, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Make JWT-specific payload.

        Args:
            exp (int | None): Token expire, if None -> use default
            data (dict[str, Any]): Data to payload

        Returns:
            dict[str, Any]: Payload
        """
        payload = {
            "iat": datetime.datetime.now().timestamp(),
            "exp": (datetime.datetime.now().timestamp() + exp) if exp else None,
            "jti": str(uuid.uuid4()),
        }
        payload = payload | data
        return payload

    async def jwt_create_token(self, payload: dict[str, Any]) -> str:
        """Create JWT token.

        Args:
            payload (dict[str, Any]): Data payload

        Returns:
            str: New token
        """
        return fake_jwt_token(payload)

    async def jwt_verify_token(
        self, token: str, check_exp: bool = True, check_list: bool = True
    ) -> dict[str, Any]:
        """Verify and decode JWT token.

        Args:
            token (str): JWT token
            check_exp (bool): Check expire
            check_list (bool): Check white/black list

        Returns:
            dict[str, Any]: Decoded payload

        Raises:
            ValueError: If the token format is invalid.
        """
        try:
            headers, payload, _ = token.split(".")
            headers = json.loads(base64url_decode(headers).decode("utf-8"))
            payload = base64url_decode(payload).decode("utf-8")

            if headers.get("typ") == "fake-JWT":
                return json.loads(payload)
            else:
                raise ValueError("Invalid token format.")
        except (ValueError, IndexError, json.JSONDecodeError) as e:
            raise ValueError("Invalid token format.") from e

    async def session_create(
        self, session_key: str, data: dict[str, Any]
    ) -> str:
        """Create new session.

        Args:
            session_key (str): Key for session
            data (dict[str, Any]): Session data

        Returns:
            str: New session ID
        """
        session_id = generate_session_id()
        self._sessions[session_id] = data.copy()
        self._session_keys[session_id] = session_key
        return session_id

    async def session_get(self, session_id: str) -> dict[str, Any] | None:
        """Get data from session.

        Args:
            session_id (str): Session ID

        Returns:
            dict[str, Any] | None: Session data if exist
        """
        return self._sessions.get(session_id)

    async def session_delete(self, session_id: str) -> None:
        """Delete session.

        Args:
            session_id (str): Session ID
        """
        self._sessions.pop(session_id, None)
        self._session_keys.pop(session_id, None)

    async def session_update(
        self, session_id: str, data: dict[str, Any]
    ) -> None:
        """Update session data.

        Args:
            session_id (str): Session ID
            data (dict[str, Any]): New data
        """
        if session_id in self._sessions:
            self._sessions[session_id].update(data)

    async def session_clear(self, session_key: str) -> None:
        """Delete all sessions by key.

        Args:
            session_key (str): Key of session
        """
        to_delete = [
            session_id
            for session_id, key in self._session_keys.items()
            if key == session_key
        ]
        for session_id in to_delete:
            self._sessions.pop(session_id, None)
            self._session_keys.pop(session_id, None)

    async def session_rework(self, old_session_id: str) -> str:
        """Rework session.

        Args:
            old_session_id (str): Old session id

        Returns:
            str: New session id
        """
        if old_session_id not in self._sessions:
            session_id = generate_session_id()
            self._sessions[session_id] = {}
            return session_id

        old_data = self._sessions[old_session_id].copy()
        old_key = self._session_keys.get(old_session_id, "default")
        new_session_id = generate_session_id()

        self._sessions[new_session_id] = old_data
        self._session_keys[new_session_id] = old_key

        return new_session_id

    async def otp_code(
        self, secret: str | bytes, factor: int | None = None
    ) -> str:
        """Generates an OTP.

        Args:
            secret (str | bytes): User secret key.
            factor (int | None, optional): Unixtime for TOTP(if none, use now time) / Counter for HOTP.

        Returns:
            str: OTP code (fixed-length string).
        """
        return "123456"

    async def otp_uri(
        self,
        secret: str,
        name: str | None = None,
        issuer: str | None = None,
        counter: int | None = None,
    ) -> str:
        """Generates an otpauth:// URI for Google Authenticator.

        Args:
            secret (str): User secret key.
            name (str): Account name (e.g., email).
            issuer (str): Service name (e.g., "GitHub").
            counter (int | None, optional): Counter (for HOTP). Default is None.

        Returns:
            str: A string of the form "otpauth://..."
        """
        uri = f"otpauth://totp/{name or 'user'}?secret={secret}"
        if issuer:
            uri += f"&issuer={issuer}"
        if counter is not None:
            uri += f"&counter={counter}"
        return uri

    async def otp_verify_code(
        self,
        secret: str | bytes,
        code: str,
        factor: int | None = None,
        look_ahead: int | None = 1,
    ) -> bool:
        """Checks the OTP code, taking into account the acceptable window.

        Args:
            secret (str | bytes): User secret key.
            code (str): The code entered.
            factor (int | None, optional): Unixtime for TOTP(if none, use now time) / Counter for HOTP.
            look_ahead (int, optional): Acceptable deviation in intervals (±window(totp) / ±look ahead(hotp)). Default is 1.

        Returns:
            bool: True if the code matches, otherwise False.
        """
        return code == "123456"

    async def oauth2_get_authorized_url(
        self, provider: str, scope: list[str], **extra_params: Any
    ) -> str:
        """Generate full OAuth2 authorization URL.

        Args:
            provider (str): Provider name
            scope (list[str]): Auth scope
            extra_params (Any): Extra auth params

        Returns:
            str: Authorization url
        """
        return f"https://{provider}/auth&client_id=TEST_CLIENT&redirect_uri=https%3A%2F%2Fexample.com&response_type=code"

    async def oauth2_fetch_token(
        self,
        provider: str,
        code: str,
        grant_type: str = "authorization_code",
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Exchange authorization code for access token.

        Args:
            provider (str): Provider name
            code (str): OAuth2 code
            grant_type (str): Type of oauth2 grant
            extra_params (Any): Extra auth params if needed

        Returns:
            dict: OAuth2 token
        """
        return {
            "access_token": fake_oauth2_token(),
            "access_expire": 9999999,
            "refresh_token": fake_oauth2_token(),
            "refresh_expire": 999999,
            "token_type": "bearer",
        }

    async def oauth2_refresh_token(
        self,
        provider: str,
        refresh_token: str,
        grant_type: str = "refresh_token",
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Use refresh token to obtain a new access token.

        Args:
            provider (str): Provider name
            refresh_token (str): Refresh token
            grant_type (str): Grant type
            extra_params (Any): Extra auth params if needed

        Returns:
            dict: Refresh token
        """
        return {
            "access_token": fake_oauth2_token(),
            "access_expire": 9999999,
            "refresh_token": fake_oauth2_token(),
            "refresh_expire": 999999,
            "token_type": "bearer",
        }

    async def oauth2_client_credentials_flow(
        self,
        provider: str,
        scope: list[str] | None = None,
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Obtain access token using client credentials flow (no user interaction).

        Args:
            provider (str): OAuth2 provider
            scope (list[str] | None): Auth scope
            extra_params (Any): Extra auth params if needed

        Returns:
            dict: JSON with access token
        """
        return {
            "access_token": fake_oauth2_token(),
            "access_expire": 9999999,
            "refresh_token": fake_oauth2_token(),
            "refresh_expire": 999999,
            "token_type": "bearer",
        }

    async def paseto_make_payload(
        self, exp: int | None = None, **data: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate payload for PASETO.

        Args:
            exp (int | None): Custom expire if needed
            data (dict[str, Any]): Data in payload

        Returns:
            dict[str, Any]: New payload
        """
        from jam.paseto.utils import payload_maker

        return payload_maker(expire=exp, data=data)

    async def paseto_create(
        self,
        payload: dict[str, Any],
        footer: dict[str, Any] | str | None,
    ) -> str:
        """Create new PASETO.

        Args:
            payload (dict[str, Any]): Payload
            footer (dict | str  | None): Footer

        Returns:
            str: New token
        """
        return fake_paseto_token(payload, footer)

    async def paseto_decode(
        self, token: str, check_exp: bool = True, check_list: bool = True
    ) -> dict[str, str | dict | None]:
        """Decode PASETO.

        Args:
            token (str): Token
            check_exp (bool): Check exp in payload
            check_list (bool): Check token in list

        Returns:
            dict: {'payload' PAYLOAD, 'footer': FOOTER}
        """
        try:
            parts = token.split(".")
            if len(parts) < 3:
                raise ValueError("Invalid PASETO token format")

            if parts[0] not in ("v1", "v2", "v3", "v4"):
                raise ValueError("Invalid PASETO version")

            payload_part = parts[2]
            footer_part = parts[3] if len(parts) > 3 else None

            payload = json.loads(base64url_decode(payload_part).decode("utf-8"))

            footer = None
            if footer_part:
                try:
                    footer = json.loads(
                        base64url_decode(footer_part).decode("utf-8")
                    )
                except (json.JSONDecodeError, UnicodeDecodeError):
                    footer = base64url_decode(footer_part).decode("utf-8")

            return {"payload": payload, "footer": footer}
        except (
            ValueError,
            IndexError,
            json.JSONDecodeError,
            UnicodeDecodeError,
        ) as e:
            raise ValueError("Invalid PASETO token format.") from e
