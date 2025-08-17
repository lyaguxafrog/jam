# -*- coding: utf-8 -*-

import datetime
import json
from typing import Callable, Optional
from uuid import uuid4


try:
    from redis import Redis
except ImportError:
    raise ImportError(
        "Redis module is not installed. Please install it with 'pip install jamlib[redis]'."
    )

from jam.__logger__ import logger
from jam.exceptions import SessionNotFoundError
from jam.sessions.modules.__abc_session_repo__ import BaseSessionModule


class RedisSessions(BaseSessionModule):
    """Redis session management module."""

    def __init__(
        self,
        redis_uri: str = "redis://localhost:6379/0",
        redis_sessions_key: str = "sessions",
        default_ttl: Optional[int] = 3600,
        is_session_crypt: bool = False,
        session_aes_secret: Optional[bytes] = None,
        id_factory: Callable[[], str] = lambda: str(uuid4()),
    ) -> None:
        """Initialize the Redis session management module.

        Args:
            redis_uri (str): The URI for the Redis server.
            redis_sessions_key (str): The key under which sessions are stored in Redis.
            default_ttl (Optional[int]): Default time-to-live for sessions in seconds. Defaults to 3600 seconds (1 hour).
            is_session_crypt (bool): If True, session keys will be encoded.
            session_aes_secret (Optional[bytes]): AES secret for encoding session keys. Required if `is_session_key_crypt` is True.
            id_factory (Callable[[], str], optional): A callable that generates unique IDs. Defaults to a UUID factory.
        """
        super().__init__(
            id_factory=id_factory,
            is_session_crypt=is_session_crypt,
            session_aes_secret=session_aes_secret,
        )
        self._redis = Redis.from_url(redis_uri, decode_responses=True)
        logger.debug("Redis connection established at %s", redis_uri)

        self.ttl = default_ttl
        self.session_path = redis_sessions_key

    def _ping(self) -> bool:
        """Check if the Redis connection is alive."""
        try:
            return self._redis.ping()
        except Exception as e:
            logger.error("Redis ping failed: %s", e)
            return False

    def create(self, session_key: str, data: dict) -> str:
        """Create a new session with the given session key and data.

        Args:
            session_key (str): The key for the session.
            data (dict): The data to be stored in the session.

        Returns:
            str: The unique ID of the created session.
        """
        session_id = self.id
        if self.ttl:
            data["_session_exp"] = (
                datetime.datetime.now().timestamp() + self.ttl
            )
        self._redis.hset(
            name=f"{self.session_path}:{session_key}",
            key=session_id,
            value=json.dumps(data),
        )

        if hasattr(self, "_code_session_key"):
            session_id = self._encode_session_id(f"{session_key}:{session_id}")
            return session_id

        return f"{session_key}:{session_id}"

    def get(
        self, session_id: str, delete_if_expire: bool = True
    ) -> dict | None:
        """Retrieve a session by its key or ID.

        Args:
            session_id (str): The session key or ID.
            delete_if_expire (bool): If True, delete the session if it has expired. Defaults to True.

        Returns:
            dict | None: The session data if found, otherwise None.
        """
        if hasattr(self, "_code_session_key"):
            try:
                session_id = self._decode_session_id(session_id)
            except ValueError as e:
                logger.error("Failed to decode session ID: %s", e)
                return None

        session_key, session_id_ = session_id.split(":", 1)
        data = self._redis.hget(
            f"{self.session_path}:{session_key}", session_id_
        )

        if not data:
            return None

        data = json.loads(data)
        if (
            "_session_exp" in data
            and datetime.datetime.now().timestamp() > data["_session_exp"]
        ):
            if delete_if_expire:
                self.delete(session_id)
            return None

        return data

    def delete(self, session_id: str) -> None:
        """Delete a session by its ID.

        Args:
            session_id (str): The session ID.
        """
        if hasattr(self, "_code_session_key"):
            try:
                session_id = self._decode_session_id(session_id)
            except ValueError as e:
                logger.error("Failed to decode session ID: %s", e)
                return

        session_key, session_id = session_id.split(":", 1)
        self._redis.hdel(f"{self.session_path}:{session_key}", session_id)
        logger.debug("Session %s deleted successfully.", session_id)

    def clear(self, session_key: str) -> None:
        """Clear all sessions for a given session key.

        Args:
            session_key (str): The session key to clear.
        """
        self._redis.delete(f"{self.session_path}:{session_key}")
        logger.debug(
            "All sessions for key '%s' cleared successfully.", session_key
        )

    def update(self, session_id: str, data: dict) -> None:
        """Update an existing session with new data.

        Args:
            session_id (str): The ID of the session to update.
            data (dict): The new data to be stored in the session.
        """
        if hasattr(self, "_code_session_key"):
            try:
                session_id = self._decode_session_id(session_id)
            except ValueError as e:
                logger.error("Failed to decode session ID: %s", e)
                return

        session_key, session_id_ = session_id.split(":", 1)
        if self.ttl:
            data["_session_exp"] = (
                datetime.datetime.now().timestamp() + self.ttl
            )
        self._redis.hset(
            name=f"{self.session_path}:{session_key}",
            key=session_id_,
            value=json.dumps(data),
        )
        logger.debug("Session %s updated successfully.", session_id_)

    def rework(self, session_id: str) -> str:
        """Rework a session and return its new ID.

        Args:
            session_id (str): The ID of the session to rework.

        Returns:
            str: The new session ID.
        """
        if hasattr(self, "_code_session_key"):
            try:
                session_id = self._decode_session_id(session_id)
            except ValueError as e:
                SessionNotFoundError(f"Failed to decode session ID: {e}")

        session_key, old_session_id = session_id.split(":", 1)
        data = self.get(session_id)

        if not data:
            raise SessionNotFoundError(
                f"Session with ID {session_id} not found."
            )

        new_session_id = self.create(session_key, data)
        self.delete(session_id)
        logger.debug("Session %s reworked to %s.", session_id, new_session_id)

        return new_session_id
