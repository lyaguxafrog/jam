# -*- coding: utf-8 -*-

import json
from collections.abc import Callable
from typing import Optional, Union
from uuid import uuid4

from redis.asyncio import Redis

from jam.__logger__ import logger
from jam.exceptions import SessionNotFoundError
from jam.sessions.redis import RedisSessions as SyncRedisSessions


class RedisSessions(SyncRedisSessions):
    """Async redis sessions module.

    Dependency required:
    `pip install jamlib[redis]`
    """

    def __init__(
        self,
        redis_uri: Union[str, Redis] = "redis://localhost:6379/0",
        redis_sessions_key: str = "sessions",
        default_ttl: Optional[int] = 3600,
        is_session_crypt: bool = False,
        session_aes_secret: Optional[bytes] = None,
        id_factory: Callable[[], str] = lambda: str(uuid4()),
    ) -> None:
        """Initialize the Redis session management module.

        Args:
            redis_uri (str | Redis): The URI for the Redis server.
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
        if isinstance(redis_uri, str):
            self._redis = Redis.from_url(redis_uri, decode_responses=True)
        else:
            self._redis = redis_uri
        logger.debug("Redis connection established at %s", redis_uri)

        self.ttl = default_ttl
        self.session_path = redis_sessions_key

    async def _ping(self) -> bool:
        try:
            return await self._redis.ping()
        except Exception as e:
            logger.error("Redis ping failed %s", e)
            return False

    async def create(self, session_key: str, data: dict) -> str:
        """Create a new session with the given session key and data.

        Args:
            session_key (str): The key for the session.
            data (dict): The data to be stored in the session.

        Returns:
            str: The unique ID of the created session.
        """
        session_id = self.__encode_session_id_if_needed__(
            f"{session_key}:{self.id}"
        )
        logger.debug("Gen session: %s", session_id)

        try:
            dumps_data = self.__encode_session_data__(data)
        except AttributeError:
            dumps_data = json.dumps(data)
        del data

        await self._redis.hset(
            name=f"{self.session_path}:{session_key}",
            key=session_id,
            value=dumps_data,
        )
        logger.debug("Set session %s successfully.", session_id)
        if self.ttl:
            await self._redis.hexpire(
                f"{self.session_path}:{session_key}", self.ttl, session_id
            )
            logger.debug(
                "Set TTL for session %s to $d seconds.", session_id, self.ttl
            )

        return session_id

    async def get(self, session_id: str) -> Optional[dict]:
        """Retrieve a session by its key or ID.

        Args:
            session_id (str): The session key or ID.

        Returns:
            dict | None: The session data if found, otherwise None.
        """
        decode_session_key = self.__decode_session_id_if_needed__(
            session_id
        ).split(":", 1)
        session = await self._redis.hget(
            name=f"{self.session_path}:{decode_session_key[0]}", key=session_id
        )
        if not session:
            logger.debug("Session %s not found.", session_id)
            return None

        try:
            loads_data = self.__decode_session_data__(session)
        except AttributeError:
            loads_data = json.loads(session)
        del session

        return loads_data

    async def delete(self, session_id: str) -> None:
        """Delete a session by its ID.

        Args:
            session_id (str): The session ID.
        """
        decoded_session_key = self.__decode_session_id_if_needed__(
            session_id
        ).split(":", 1)
        await self._redis.hdel(
            f"{self.session_path}:{decoded_session_key[0]}",
            session_id,
        )

    async def clear(self, session_key: str) -> None:
        """Clear all sessions for a given session key.

        Args:
            session_key (str): The session key to clear.
        """
        await self._redis.delete(f"{self.session_path}:{session_key}")
        logger.debug(
            "All sessions for key '%s' cleared successfully.", session_key
        )

    async def update(self, session_id: str, data: dict) -> None:
        """Update an existing session with new data.

        Args:
            session_id (str): The ID of the session to update.
            data (dict): The new data to be stored in the session.
        """
        decoded_session_key = self.__decode_session_id_if_needed__(
            session_id
        ).split(":", 1)
        if not await self.get(session_id):
            raise SessionNotFoundError(
                f"Session with ID {session_id} not found."
            )

        try:
            dumps_data = self.__encode_session_data__(data)
        except AttributeError:
            dumps_data = json.dumps(data)
        del data

        await self._redis.hset(
            name=f"{self.session_path}:{decoded_session_key[0]}",
            key=session_id,
            value=dumps_data,
        )
        logger.debug("Session %s updated successfully.", session_id)

        if self.ttl:
            await self._redis.hexpire(
                f"{self.session_path}:{decoded_session_key[0]}",
                self.ttl,
                session_id,
            )
            logger.debug(
                "TTL for session %s reset to %d seconds.", session_id, self.ttl
            )

    # TODO: Optimize this method
    async def rework(self, session_id: str) -> str:
        """Rework a session and return its new ID.

        Args:
            session_id (str): The ID of the session to rework.

        Returns:
            str: The new session ID.
        """
        decoded_session_key = self.__decode_session_id_if_needed__(
            session_id
        ).split(":", 1)
        session_data = await self.get(session_id)
        if not session_data:
            raise SessionNotFoundError(
                f"Session with ID {session_id} not found."
            )

        new_session_id = await self.create(decoded_session_key[0], session_data)

        await self.delete(session_id)
        return new_session_id
