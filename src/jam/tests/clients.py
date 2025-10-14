# -*- coding: utf-8 -*-

import json
from typing import Any, Optional, Union

from jam.aio import Jam as AioJam
from jam.instance import Jam
from jam.jwt.tools import __base64url_decode__
from jam.tests.fakers import fake_jwt_token, fake_oauth2_token


class TestJam(Jam):
    """A test client for Jam.

    Examples:
        ```python
        import pytest
        from jam.tests import TestJam
        from jam.tests.fakers import invalid_token

        @pytest.fixture
        def client() -> TestJam:
            return TestJam()

        def test_gen_jwt_token(client) -> None:
            payload = {"user_id": 1, "role": "admin"}
            token = client.gen_jwt_token(payload)
            assert isinstance(token, str)
            assert token.count(".") == 2  # JWT tokens have two dots

        def test_verify_jwt_token(client) -> None:
            payload = {"user_id": 1, "role": "admin"}
            token = client.gen_jwt_token(payload)
            verified_payload = client.verify_jwt_token(token, check_exp=False, check_list=False)
            assert verified_payload == payload

        def test_invalid_jwt_token(client) -> None:
            token = invalid_token()
            with pytest.raises(ValueError):
                client.verify_jwt_token(token, check_exp=False, check_list=False)
        ```
    """

    __test__ = False

    def __init__(
        self,
        config: Optional[Union[str, dict[str, Any]]] = None,
        pointer: str = "jam",
    ) -> None:
        """Class constructor.

        Args:
            config (str | dict[str, Any] | None): Jam configuration.
            pointer (str): Pointer for the client instance.
        """
        self.module = self
        self._fake_session: dict[str, Any] = {}

    def jwt_create_token(self, payload: dict[str, Any]) -> str:
        """Generate a fake JWT token for testing purposes.

        This token ALWAYS validates successfully.

        Args:
            payload (dict[str, Any]): Payload to include in the JWT token.

        Returns:
            str: A fake JWT token.
        """
        return fake_jwt_token(payload)

    def jwt_make_payload(
        self, exp: Optional[int], data: dict[str, Any]
    ) -> dict[str, Any]:
        """Payload maker tool.

        Args:
            exp (int | None): Expire
            data: Arbitrary keyword arguments to include in the payload.

        Returns:
            dict[str, Any]: A dictionary representing the payload.
        """
        return data

    def jwt_verify_token(
        self, token: str, check_exp: bool = True, check_list: bool = True
    ) -> dict[str, Any]:
        """Verify JWT token.

        Args:
            token (str): JWT token to verify.
            check_exp (bool): Whether to check the expiration time.
            check_list (bool): Whether to check against a blacklist.

        Returns:
            dict[str, Any]: The payload of the verified JWT token.

        Raises:
            ValueError: If the token format is invalid.
        """
        headers, payload, _ = token.split(".")
        headers = json.loads(__base64url_decode__(headers).decode("utf-8"))
        payload = __base64url_decode__(payload).decode("utf-8")

        if headers["typ"] == "fake-JWT":
            return json.loads(payload)
        else:
            raise ValueError("Invalid token format.")

    def gen_jwt_token(self, payload: dict[str, Any]) -> str:
        """Generate a fake JWT token for testing purposes.

        This token ALWAYS validates successfully.

        Args:
            payload (dict[str, Any]): Payload to include in the JWT token.

        Returns:
            str: A fake JWT token.
        """
        return self.jwt_create_token(payload)

    def verify_jwt_token(
        self, token: str, check_exp: bool = True, check_list: bool = True
    ) -> dict[str, Any]:
        """Verify JWT token.

        Args:
            token (str): JWT token to verify.
            check_exp (bool): Whether to check the expiration time.
            check_list (bool): Whether to check against a blacklist.

        Returns:
            dict[str, Any]: The payload of the verified JWT token.

        Raises:
            ValueError: If the token format is invalid.
        """
        headers, payload, _ = token.split(".")
        headers = json.loads(__base64url_decode__(headers).decode("utf-8"))
        payload = __base64url_decode__(payload).decode("utf-8")

        if headers["typ"] == "fake-JWT":
            return json.loads(payload)
        else:
            raise ValueError("Invalid token format.")

    def make_payload(self, **payload: dict[str, Any]) -> dict[str, Any]:
        """Payload maker tool.

        Args:
            **payload: Arbitrary keyword arguments to include in the payload.

        Returns:
            dict[str, Any]: A dictionary representing the payload.
        """
        return payload

    def session_create(self, session_key: str, data: dict[str, Any]) -> str:
        """Create new session.

        Args:
            session_key (str): The key for the session.
            data (dict): The data to store in the session.

        Returns:
            str: A fake session ID.
        """
        self._fake_session = data
        return "fake-session-id"

    def create_session(self, session_key: str, data: dict[str, Any]) -> str:
        """Create new session.

        Args:
            session_key (str): The key for the session.
            data (dict): The data to store in the session.

        Returns:
            str: A fake session ID.
        """
        self._fake_session = data
        return "fake-session-id"

    def session_get(self, session_id: str) -> Optional[dict[str, Any]]:
        """Retrieve session data by session ID.

        Args:
            session_id (str): The ID of the session to retrieve.

        Returns:
            dict | None: The session data if found, otherwise None.
        """
        if session_id == "fake-session-id":
            return self._fake_session
        return None

    def get_session(self, session_id: str) -> Optional[dict[str, Any]]:
        """Retrieve session data by session ID.

        Args:
            session_id (str): The ID of the session to retrieve.

        Returns:
            dict | None: The session data if found, otherwise None.
        """
        if session_id == "fake-session-id":
            return self._fake_session
        return None

    def session_delete(self, session_id: str) -> None:
        """Delete a session by its ID.

        Args:
            session_id (str): The ID of the session to delete.
        """
        ...

    def delete_session(self, session_id: str) -> None:
        """Delete a session by its ID.

        Args:
            session_id (str): The ID of the session to delete.
        """
        ...

    def session_update(self, session_id: str, data: dict[str, Any]) -> None:
        """Update session data by session ID.

        Args:
            session_id (str): The ID of the session to update.
            data (dict): The new data for the session.
        """
        if session_id == "fake-session-id":
            self._fake_session.update(data)
        else:
            ...

    def update_session(self, session_id: str, data: dict) -> None:
        """Update session data by session ID.

        Args:
            session_id (str): The ID of the session to update.
            data (dict): The new data for the session.
        """
        if session_id == "fake-session-id":
            self._fake_session.update(data)
        else:
            ...

    def session_clear(self, session_key: str) -> None:
        """Clear all sessions associated with a specific session key.

        Args:
            session_key (str): The session key whose sessions are to be cleared.
        """
        ...

    def clear_sessions(self, session_key: str) -> None:
        """Clear all sessions associated with a specific session key.

        Args:
            session_key (str): The session key whose sessions are to be cleared.
        """
        ...

    def session_rework(self, old_session_id: str) -> str:
        """Rework an existing session key to a new one.

        Args:
            old_session_id (str): The old session id to be reworked.

        Returns:
            str: A new fake session ID.
        """
        return "fake-session-id"

    def rework_session(self, old_session_key: str) -> str:
        """Rework an existing session key to a new one.

        Args:
            old_session_key (str): The old session key to be reworked.

        Returns:
            str: A new fake session ID.
        """
        return "fake-session-id"

    def otp_code(
        self, secret: Union[str, bytes], factor: Optional[int] = None
    ) -> str:
        """Generates a OTP code.

        Args:
            secret (str): The secret key used to generate the OTP code.
            factor (int | None): An optional factor to influence the OTP generation.

        Returns:
            str: A fake OTP code.
        """
        return "123456"

    def get_otp_code(self, secret: str, factor: Optional[int] = None) -> str:
        """Generates a OTP code.

        Args:
            secret (str): The secret key used to generate the OTP code.
            factor (int | None): An optional factor to influence the OTP generation.

        Returns:
            str: A fake OTP code.
        """
        return "123456"

    def otp_verify_code(
        self,
        secret: Union[str, bytes],
        code: str,
        factor: Optional[int] = None,
        look_ahead: Optional[int] = 1,
    ) -> bool:
        """Verifies a given OTP code.

        Args:
            secret (str): The secret key used to verify the OTP code.
            code (str): The OTP code to verify.
            factor (int | None): An optional factor that was used during OTP generation.
            look_ahead (int | None): An optional look-ahead window for verification.

        Returns:
            bool: True if the OTP code is valid, False otherwise.
        """
        return code == "123456"

    def verify_otp_code(
        self,
        secret: str,
        code: str,
        factor: Optional[int] = None,
        look_ahead: Optional[int] = None,
    ) -> bool:
        """Verifies a given OTP code.

        Args:
            secret (str): The secret key used to verify the OTP code.
            code (str): The OTP code to verify.
            factor (int | None): An optional factor that was used during OTP generation.
            look_ahead (int | None): An optional look-ahead window for verification.

        Returns:
            bool: True if the OTP code is valid, False otherwise.
        """
        return code == "123456"

    def otp_uri(
        self,
        secret: str,
        name: Optional[str] = None,
        issuer: Optional[str] = None,
        counter: Optional[int] = None,
    ) -> str:
        """Generates an otpauth:// URI for Google Authenticator.

        Args:
            secret (str): The secret key used to generate the OTP URI.
            name (str | None): An optional name for the OTP account.
            issuer (str | None): An optional issuer for the OTP account.
            counter (int | None): An optional counter for HOTP.

        Returns:
            str: A fake otpauth:// URI.
        """
        uri = f"otpauth://totp/{name or 'user'}?secret={secret}"
        if issuer:
            uri += f"&issuer={issuer}"
        if counter is not None:
            uri += f"&counter={counter}"
        return uri

    def get_otp_uri(
        self,
        secret: str,
        name: Optional[str] = None,
        issuer: Optional[str] = None,
        counter: Optional[int] = None,
    ) -> str:
        """Generates an otpauth:// URI for Google Authenticator.

        Args:
            secret (str): The secret key used to generate the OTP URI.
            name (str | None): An optional name for the OTP account.
            issuer (str | None): An optional issuer for the OTP account.
            counter (int | None): An optional counter for HOTP.

        Returns:
            str: A fake otpauth:// URI.
        """
        uri = f"otpauth://totp/{name or 'user'}?secret={secret}"
        if issuer:
            uri += f"&issuer={issuer}"
        if counter is not None:
            uri += f"&counter={counter}"
        return uri

    def oauth2_get_authorized_url(
        self, provider: str, scope: list[str], **extra_params: Any
    ) -> str:
        """Test oauth2 URL method.

        Return FAKE url
        """
        return f"https://{provider}/auth&client_id=TEST_CLIENT&redirect_uri=https%3A%2F%2Fexample.com&response_type=code"

    def oauth2_fetch_token(
        self,
        provider: str,
        code: str,
        grant_type: str = "authorization_code",
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Fake fetch token."""
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
        """Fake refresh token."""
        return {
            "access_token": fake_oauth2_token(),
            "access_expire": 9999999,
            "refresh_token": fake_oauth2_token(),
            "refresh_expire": 999999,
            "token_type": "bearer",
        }

    def oauth2_client_credentials_flow(
        self, scope: Optional[list[str]] = None, **extra_params: Any
    ) -> dict[str, Any]:
        """Fake client MtM flow."""
        return {
            "access_token": fake_oauth2_token(),
            "access_expire": 9999999,
            "refresh_token": fake_oauth2_token(),
            "refresh_expire": 999999,
            "token_type": "bearer",
        }


class TestAsyncJam(AioJam):
    """A test async client for Jam.

    Example:
        ```python
        import pytest
        import pytest_asyncio
        import asyncio
        from jam.tests import TestAsyncJam
        from jam.tests.fakers import invalid_token

        @pytest_asyncio.fixture
        async def client() -> TestAsyncJam:
            return TestAsyncJam()

        @pytest.mark.asyncio
        async def test_gen_jwt_token(client) -> None:
            payload = {"user_id": 1, "role": "admin"}
            token = await client.gen_jwt_token(payload)
            assert isinstance(token, str)
            assert token.count(".") == 2  # JWT tokens have two dots

        @pytest.mark.asyncio
        async def test_verify_jwt_token(client) -> None:
            payload = {"user_id": 1, "role": "admin"}
            token = await client.gen_jwt_token(payload)
            verified_payload = await client.verify_jwt_token(token, check_exp=False, check_list=False)
            assert verified_payload == payload
        ```
    """

    __test__ = False

    def __init__(
        self,
        config: Optional[Union[str, dict[str, Any]]] = None,
        pointer: str = "jam",
    ) -> None:
        """Class constructor.

        Args:
            config (str | dict[str, Any] | None): Jam configuration.
            pointer (str): Pointer for the client instance.
        """
        self.module = self
        self._fake_session: dict[str, Any] = {}

    async def jwt_create_token(self, payload: dict[str, Any]) -> str:
        """Generate a fake JWT token for testing purposes.

        This token ALWAYS validates successfully.

        Args:
            payload (dict[str, Any]): Payload to include in the JWT token.

        Returns:
            str: A fake JWT token.
        """
        return fake_jwt_token(payload)

    async def gen_jwt_token(self, payload: dict[str, Any]) -> str:
        """Generate a fake JWT token for testing purposes.

        This token ALWAYS validates successfully.

        Args:
            payload (dict[str, Any]): Payload to include in the JWT token.

        Returns:
            str: A fake JWT token.
        """
        return fake_jwt_token(payload)

    async def jwt_verify_token(
        self, token: str, check_exp: bool = True, check_list: bool = True
    ) -> dict[str, Any]:
        """Verify JWT token.

        Args:
            token (str): JWT token to verify.
            check_exp (bool): Whether to check the expiration time.
            check_list (bool): Whether to check against a blacklist.

        Returns:
            dict[str, Any]: The payload of the verified JWT token.

        Raises:
            ValueError: If the token format is invalid.
        """
        headers, payload, _ = token.split(".")
        headers = json.loads(__base64url_decode__(headers).decode("utf-8"))
        payload = __base64url_decode__(payload).decode("utf-8")

        if headers["typ"] == "fake-JWT":
            return json.loads(payload)
        else:
            raise ValueError("Invalid token format.")

    async def verify_jwt_token(
        self, token: str, check_exp: bool = True, check_list: bool = True
    ) -> dict[str, Any]:
        """Verify JWT token.

        Args:
            token (str): JWT token to verify.
            check_exp (bool): Whether to check the expiration time.
            check_list (bool): Whether to check against a blacklist.

        Returns:
            dict[str, Any]: The payload of the verified JWT token.

        Raises:
            ValueError: If the token format is invalid.
        """
        headers, payload, _ = token.split(".")
        headers = json.loads(__base64url_decode__(headers).decode("utf-8"))
        payload = __base64url_decode__(payload).decode("utf-8")

        if headers["typ"] == "fake-JWT":
            return json.loads(payload)
        else:
            raise ValueError("Invalid token format.")

    async def jwt_make_payload(
        self, exp: Optional[int], data: dict[str, Any]
    ) -> dict[str, Any]:
        """Payload maker tool.

        Args:
            exp (int): Expire
            data: Arbitrary keyword arguments to include in the payload.

        Returns:
            dict[str, Any]: A dictionary representing the payload.
        """
        return data

    async def make_payload(self, **payload: dict[str, Any]) -> dict[str, Any]:
        """Payload maker tool.

        Args:
            **payload: Arbitrary keyword arguments to include in the payload.

        Returns:
            dict[str, Any]: A dictionary representing the payload.
        """
        return payload

    async def session_create(
        self, session_key: str, data: dict[str, Any]
    ) -> str:
        """Create new session.

        Args:
            session_key (str): The key for the session.
            data (dict): The data to store in the session.

        Returns:
            str: A fake session ID.
        """
        self._fake_session = data
        return "fake-session-id"

    async def create_session(
        self, session_key: str, data: dict[str, Any]
    ) -> str:
        """Create new session.

        Args:
            session_key (str): The key for the session.
            data (dict): The data to store in the session.

        Returns:
            str: A fake session ID.
        """
        self._fake_session = data
        return "fake-session-id"

    async def session_get(self, session_id: str) -> Optional[dict[str, Any]]:
        """Retrieve session data by session ID.

        Args:
            session_id (str): The ID of the session to retrieve.

        Returns:
            dict | None: The session data if found, otherwise None.
        """
        if session_id == "fake-session-id":
            return self._fake_session
        return None

    async def get_session(self, session_id: str) -> Optional[dict[str, Any]]:
        """Retrieve session data by session ID.

        Args:
            session_id (str): The ID of the session to retrieve.

        Returns:
            dict | None: The session data if found, otherwise None.
        """
        if session_id == "fake-session-id":
            return self._fake_session
        return None

    async def session_delete(self, session_id: str) -> None:
        """Delete a session by its ID.

        Args:
            session_id (str): The ID of the session to delete.
        """
        ...

    async def delete_session(self, session_id: str) -> None:
        """Delete a session by its ID.

        Args:
            session_id (str): The ID of the session to delete.
        """
        ...

    async def session_update(
        self, session_id: str, data: dict[str, Any]
    ) -> None:
        """Update session data by session ID.

        Args:
            session_id (str): The ID of the session to update.
            data (dict): The new data for the session.
        """
        if session_id == "fake-session-id":
            self._fake_session.update(data)
        else:
            ...

    async def update_session(self, session_id: str, data: dict) -> None:
        """Update session data by session ID.

        Args:
            session_id (str): The ID of the session to update.
            data (dict): The new data for the session.
        """
        if session_id == "fake-session-id":
            self._fake_session.update(data)
        else:
            ...

    async def session_clear(self, session_key: str) -> None:
        """Clear all sessions associated with a specific session key.

        Args:
            session_key (str): The session key whose sessions are to be cleared.
        """
        ...

    async def clear_sessions(self, session_key: str) -> None:
        """Clear all sessions associated with a specific session key.

        Args:
            session_key (str): The session key whose sessions are to be cleared.
        """
        ...

    async def session_rework(self, old_session_id: str) -> str:
        """Rework an existing session key to a new one.

        Args:
            old_session_id (str): The old session id to be reworked.

        Returns:
            str: A new fake session ID.
        """
        return "fake-session-id"

    async def rework_session(self, old_session_key: str) -> str:
        """Rework an existing session key to a new one.

        Args:
            old_session_key (str): The old session key to be reworked.

        Returns:
            str: A new fake session ID.
        """
        return "fake-session-id"

    async def otp_code(
        self, secret: Union[str, bytes], factor: Optional[int] = None
    ) -> str:
        """Generates a OTP code.

        Args:
            secret (str): The secret key used to generate the OTP code.
            factor (int | None): An optional factor to influence the OTP generation.

        Returns:
            str: A fake OTP code.
        """
        return "123456"

    async def get_otp_code(
        self, secret: str, factor: Optional[int] = None
    ) -> str:
        """Generates a OTP code.

        Args:
            secret (str): The secret key used to generate the OTP code.
            factor (int | None): An optional factor to influence the OTP generation.

        Returns:
            str: A fake OTP code.
        """
        return "123456"

    async def otp_verify_code(
        self,
        secret: Union[str, bytes],
        code: str,
        factor: Optional[int] = None,
        look_ahead: Optional[int] = 1,
    ) -> bool:
        """Verifies a given OTP code.

        Args:
            secret (str): The secret key used to verify the OTP code.
            code (str): The OTP code to verify.
            factor (int | None): An optional factor that was used during OTP generation.
            look_ahead (int | None): An optional look-ahead window for verification.

        Returns:
            bool: True if the OTP code is valid, False otherwise.
        """
        return code == "123456"

    async def verify_otp_code(
        self,
        secret: str,
        code: str,
        factor: Optional[int] = None,
        look_ahead: Optional[int] = None,
    ) -> bool:
        """Verifies a given OTP code.

        Args:
            secret (str): The secret key used to verify the OTP code.
            code (str): The OTP code to verify.
            factor (int | None): An optional factor that was used during OTP generation.
            look_ahead (int | None): An optional look-ahead window for verification.

        Returns:
            bool: True if the OTP code is valid, False otherwise.
        """
        return code == "123456"

    async def otp_uri(
        self,
        secret: str,
        name: Optional[str] = None,
        issuer: Optional[str] = None,
        counter: Optional[int] = None,
    ) -> str:
        """Generates an otpauth:// URI for Google Authenticator.

        Args:
            secret (str): The secret key used to generate the OTP URI.
            name (str | None): An optional name for the OTP account.
            issuer (str | None): An optional issuer for the OTP account.
            counter (int | None): An optional counter for HOTP.

        Returns:
            str: A fake otpauth:// URI.
        """
        uri = f"otpauth://totp/{name or 'user'}?secret={secret}"
        if issuer:
            uri += f"&issuer={issuer}"
        if counter is not None:
            uri += f"&counter={counter}"
        return uri

    async def get_otp_uri(
        self,
        secret: str,
        name: Optional[str] = None,
        issuer: Optional[str] = None,
        counter: Optional[int] = None,
    ) -> str:
        """Generates an otpauth:// URI for Google Authenticator.

        Args:
            secret (str): The secret key used to generate the OTP URI.
            name (str | None): An optional name for the OTP account.
            issuer (str | None): An optional issuer for the OTP account.
            counter (int | None): An optional counter for HOTP.

        Returns:
            str: A fake otpauth:// URI.
        """
        uri = f"otpauth://totp/{name or 'user'}?secret={secret}"
        if issuer:
            uri += f"&issuer={issuer}"
        if counter is not None:
            uri += f"&counter={counter}"
        return uri

    async def oauth2_get_authorized_url(
        self, provider: str, scope: list[str], **extra_params: Any
    ) -> str:
        """Test oauth2 URL method.

        Return FAKE url
        """
        return f"https://{provider}/auth&client_id=TEST_CLIENT&redirect_uri=https%3A%2F%2Fexample.com&response_type=code"

    async def oauth2_fetch_token(
        self,
        provider: str,
        code: str,
        grant_type: str = "authorization_code",
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Fake fetch token."""
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
        """Fake refresh token."""
        return {
            "access_token": fake_oauth2_token(),
            "access_expire": 9999999,
            "refresh_token": fake_oauth2_token(),
            "refresh_expire": 999999,
            "token_type": "bearer",
        }

    async def oauth2_client_credentials_flow(
        self, scope: Optional[list[str]] = None, **extra_params: Any
    ) -> dict[str, Any]:
        """Fake client MtM flow."""
        return {
            "access_token": fake_oauth2_token(),
            "access_expire": 9999999,
            "refresh_token": fake_oauth2_token(),
            "refresh_expire": 999999,
            "token_type": "bearer",
        }
