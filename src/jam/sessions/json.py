# -*- coding: utf-8 -*-

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


try:
    import tinydb
except ImportError:
    raise ImportError(
        "JSON module is not installed. Please install it with 'pip install jamlib[json]'."
    )

from jam.__logger__ import logger
from jam.exceptions.sessions import SessionNotFoundError
from jam.sessions.__abc_session_repo__ import BaseSessionModule


class JSONSessions(BaseSessionModule):
    """Session management module for JSON storage."""

    def __init__(
        self,
        json_path: str = "sessions.json",
        is_session_crypt: bool = False,
        session_aes_secret: Optional[bytes] = None,
        id_factory: Callable[[], str] = lambda: str(uuid4()),
    ) -> None:
        """Initialize the JSON session management module.

        Args:
            json_path (str): Path to the JSON file where sessions will be stored.
            is_session_crypt (bool): If True, session keys will be encoded.
            session_aes_secret (Optional[bytes]): AES secret for encoding session keys. Required if `is_session_crypt` is True.
            id_factory (Callable[[], str], optional): A callable that generates unique IDs. Defaults to a UUID factory.
        """
        super().__init__(
            is_session_crypt=is_session_crypt,
            session_aes_secret=session_aes_secret,
            id_factory=id_factory,
        )
        self._db = tinydb.TinyDB(json_path)
        self._qs = tinydb.Query()
        logger.debug("JSON database initialized at %s", json_path)

    @dataclass
    class _SessionDoc:
        key: str
        session_id: str
        data: str
        created_at: float = field(default_factory=datetime.now().timestamp)

    def create(self, session_key: str, data: dict) -> str:
        """Create a new session.

        Args:
            session_key (str): The session key.
            data (dict): The data to be stored in the session.

        Returns:
            str: The ID of the created session.
        """
        session_id = self.__encode_session_id_if_needed__(self.id)

        try:
            dumps_data = self.__encode_session_data__(data)
        except AttributeError:
            dumps_data = json.dumps(data)
        del data

        doc = self._SessionDoc(
            key=session_key,
            session_id=session_id,
            data=dumps_data,
        )

        self._db.insert(doc.__dict__)
        logger.debug("Session created with ID %s", session_id)
        return session_id

    def get(self, session_id) -> Optional[dict]:
        """Retrieve session data by session ID.

        Args:
            session_id (str): The ID of the session to retrieve.

        Returns:
            dict | None: The session data if found, otherwise None.
        """
        # session_id = self.__decode_session_id_if_needed__(session_id)
        result = self._db.search(self._qs.session_id == session_id)
        if result:
            try:
                loads_data = self.__decode_session_data__(result[0]["data"])
            except AttributeError:
                loads_data = json.loads(result[0]["data"])
            del result
            return loads_data
        return None

    def delete(self, session_id: str) -> None:
        """Delete a session by its ID.

        Args:
            session_id (str): The ID of the session to delete.

        Returns:
            None
        """
        self._db.remove(self._qs.session_id == session_id)
        logger.debug("Session with ID %s deleted", session_id)

    def update(self, session_id: str, data: dict) -> None:
        """Update session data by its ID.

        Args:
            session_id (str): The ID of the session to update.
            data (dict): The new data to store in the session.

        Returns:
            None
        """
        try:
            dumps_data = self.__encode_session_data__(data)
        except AttributeError:
            dumps_data = json.dumps(data)
        del data

        self._db.update({"data": dumps_data}, self._qs.session_id == session_id)
        logger.debug("Session with ID %s updated", session_id)

    def clear(self, session_key: str) -> None:
        """Clear all sessions for a given session key.

        Args:
            session_key (str): The session key to clear.

        Returns:
            None
        """
        self._db.remove(self._qs.key == session_key)

    def rework(self, session_id: str) -> str:
        """Rework (regenerate) a session ID.

        Args:
            session_id (str): The current session ID to be reworked.

        Raises:
            SessionNotFoundError: If session not found

        Returns:
            str: The new session ID.
        """
        result = self._db.search(self._qs.session_id == session_id)
        if not result:
            raise SessionNotFoundError(
                f"Session with ID {session_id} not found."
            )

        new_session_id = self.__encode_session_id_if_needed__(self.id)
        self._db.update(
            {"session_id": new_session_id},
            self._qs.session_id == session_id,
        )
        logger.debug("Session ID %s reworked to %s", session_id, new_session_id)
        return new_session_id
