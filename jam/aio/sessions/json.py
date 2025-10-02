# -*- coding: utf-8 -*-

from asyncio import to_thread
from typing import Optional

from jam.sessions.json import JSONSessions as SyncJSONSessions


class JSONSessions(SyncJSONSessions):
    """Async session management module for JSON storage.

    Dependency required:
    `pip install jamlib[json]`
    """

    async def create(self, session_key: str, data: dict) -> str:
        """Create a new session.

        Args:
            session_key (str): The session key.
            data (dict): The data to be stored in the session.

        Returns:
            str: The ID of the created session.
        """
        return await to_thread(super().create, session_key, data)

    async def get(self, session_id) -> Optional[dict]:
        """Retrieve session data by session ID.

        Args:
            session_id (str): The ID of the session to retrieve.

        Returns:
            dict | None: The session data if found, otherwise None.
        """
        return await to_thread(super().get, session_id)

    async def delete(self, session_id: str) -> None:
        """Delete a session by its ID.

        Args:
            session_id (str): The ID of the session to delete.

        Returns:
            None
        """
        return await to_thread(super().delete, session_id)

    async def update(self, session_id: str, data: dict) -> None:
        """Update session data by its ID.

        Args:
            session_id (str): The ID of the session to update.
            data (dict): The new data to store in the session.

        Returns:
            None
        """
        return await to_thread(super().update, session_id, data)

    async def clear(self, session_key: str) -> None:
        """Clear all sessions for a given session key.

        Args:
            session_key (str): The session key to clear.

        Returns:
            None
        """
        return await to_thread(super().clear, session_key)

    async def rework(self, session_id: str) -> str:
        """Rework (regenerate) a session ID.

        Args:
            session_id (str): The current session ID to be reworked.

        Raises:
            SessionNotFoundError: If session not found

        Returns:
            str: The new session ID.
        """
        return await to_thread(super().rework, session_id)
