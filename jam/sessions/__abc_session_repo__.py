# -*- coding: utf-8 -*-

import json
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, Optional
from uuid import uuid4

from cryptography.fernet import Fernet

from jam.__logger__ import logger


class BaseSessionModule(ABC):
    """Abstract base class for session management modules.

    You can create your own module for sessions. For example:

    ```python
    from jam.sessions import BaseSessionModule

    class CustomSessionModule(BaseSessionModule):
        def __init__(self, some_param: str) -> None:
            super().__init__(
                is_session_crypt=True,
                session_aes_secret=b'your-32-byte-base64-encoded-key'
            )

        # Your initialization code here
        def create(session_key: str) -> str:
            ...

        def get(session_id: str) -> dict:
            ...

        def delete(session_id: str) -> None:
            ...

        def update(session_id: str, data: dict) -> None:
            ...

        def rework(session_id: str) -> str:
            ...

        def clear(session_key: str) -> None:
            ...
    ```
    """

    def __init__(
        self,
        id_factory: Callable[[], str] = lambda: str(uuid4()),
        is_session_crypt: bool = False,
        session_aes_secret: Optional[bytes] = None,
    ) -> None:
        """Class constructor.

        Args:
            id_factory (Callable[str], optional): A callable that generates unique IDs. Defaults to a UUID factory.
            is_session_crypt (bool, optional): If True, session keys will be encoded. Defaults to False.
            session_aes_secret (Optional[bytes], optional): AES secret for encoding session keys.
        """
        self._id = id_factory
        self._sk_mark_symbol = "J$_"
        if is_session_crypt and not session_aes_secret:
            raise ValueError(
                "If 'code_session_key' is True, 'session_key_aes_secret' must be provided."
            )
        if is_session_crypt:
            self._code_session_key = Fernet(session_aes_secret)

    def _encode_session_id(self, data: str) -> str:
        """Encode the session using AES encryption."""
        if not hasattr(self, "_code_session_key"):
            raise AttributeError("Session key encoding is not enabled.")
        return f"{self._sk_mark_symbol}{self._code_session_key.encrypt(data.encode()).decode()}"

    def _decode_session_id(self, data: str) -> str:
        """Decode the session using AES decryption."""
        if not hasattr(self, "_code_session_key"):
            raise AttributeError("Session key encoding is not enabled.")
        if not data.startswith(self._sk_mark_symbol):
            raise ValueError("Session key is not encoded or is invalid.")
        return self._code_session_key.decrypt(
            data[len(self._sk_mark_symbol) :].encode()
        ).decode()

    def _encode_session_id_if_needed(self, data: str) -> str:
        """Encode the session ID if it is not already encoded."""
        if hasattr(self, "_code_session_key"):
            try:
                data = self._encode_session_id(data)
            except ValueError as e:
                logger.error("Failed to encode session ID: %s", e)
            return data
        else:
            return data

    def _decode_session_id_if_needed(self, data: str) -> str:
        """Decode the session ID if it is encoded."""
        if hasattr(self, "_code_session_key"):
            try:
                data = self._decode_session_id(data)
            except ValueError as e:
                logger.error("Failed to decode session ID: %s", e)
            return data
        else:
            return data

    def _encode_session_data(self, data: dict) -> str:
        """Encode session data."""
        if not hasattr(self, "_code_session_key"):
            raise AttributeError("Session data encoding is not enabled.")

        data_json = json.dumps(data)
        return self._encode_session_id(data_json)

    def _decode_session_data(self, data: str) -> dict:
        """Decode session data."""
        if not hasattr(self, "_code_session_key"):
            raise AttributeError("Session key encoding is not enabled.")
        data = self._decode_session_id(data)
        return json.loads(data)

    @property
    def id(self) -> str:
        """Return the unique ID use id_factory."""
        return self._id()

    @abstractmethod
    def create(self, session_key: str, data: dict) -> str:
        """Create a new session with the given session key and data.

        Args:
            session_key (str): The key for the session.
            data (dict): The data to be stored in the session.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, session_id: str) -> Any:
        """Retrieve a session by its key or ID.

        Args:
            session_id (str): The ID of the session.

        Returns:
            Any: The session data if found, otherwise None.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, session_id: str) -> None:
        """Delete a session by its key or ID.

        Args:
            session_id (str): The ID of the session.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, session_id: str, data: dict) -> None:
        """Update an existing session with new data.

        Args:
            session_id (str): The ID of the session to update.
            data (dict): The new data to be stored in the session.
        """
        raise NotImplementedError

    @abstractmethod
    def rework(self, session_id: str) -> str:
        """Rework a session and return its new ID.

        Args:
            session_id (str): The ID of the session to rework.

        Returns:
            str: The new session ID.
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self, session_key: str) -> None:
        """Clear all sessions by key.

        Args:
            session_key (str): The key for the sessions to clear.
        """
        raise NotImplementedError
