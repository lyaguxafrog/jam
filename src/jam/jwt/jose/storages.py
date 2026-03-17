# -*- coding: utf-8 -*-

import os
from typing import Any, Literal

from jam.__base_encoder__ import BaseEncoder
from jam.encoders import JsonEncoder
from jam.jwt.jose.__base_storage__ import BaseStorage
from jam.logger import BaseLogger, logger


class MemmoryStorage(BaseStorage):
    """In-memory storage."""

    def __init__(self, logger: BaseLogger = logger) -> None:
        """Initialize the in-memory storage."""
        self._logger = logger
        self.__store = {}

    def get(self, name: str) -> dict[str, Any] | None:
        """Get a key by name.

        Args:
            name (str): The name of the key.

        Returns:
            str: The key data, or None if not found.
        """
        self._logger.debug(f"Getting key {name}")
        return self.__store.get(name)

    def store(self, name: str, data: dict[str, Any]) -> None:
        """Store a key with the given name and data.

        Args:
            name (str): The name of the key.
            data (dict[str, Any]): The key data.
        """
        self._logger.debug(f"Storing key {name}")
        self.__store[name] = data

    def delete(self, name: str) -> None:
        """Delete a key by name.

        Args:
            name (str): The name of the key to delete.
        """
        self._logger.debug(f"Deleting key {name}")
        self.__store.pop(name, None)


class JSONStorage(BaseStorage):
    """JSON file storage."""

    def __init__(
        self,
        path: str,
        create_dir: bool = False,
        access_mode: Literal["r", "rb", "r+", "rb+"] = "r+",
        logger: BaseLogger = logger,
        seralizer: type[BaseEncoder] | BaseEncoder = JsonEncoder,
    ) -> None:
        """Initialize the JSON storage.

        Args:
            path (str): The path to the JSON file.
            create_dir (bool): Whether to create the directory if it doesn't exist.
            access_mode (str): The file access mode.
            logger (BaseLogger): The logger to use.
            seralizer (type[BaseEncoder] | BaseEncoder): The serializer to use.
        """
        self._logger = logger
        self.path = path
        self._access_mode = access_mode
        self._seralizer = seralizer
        self._touch(path, create_dir)
        self.__hook = open(path, access_mode)

    def _touch(self, path: str, create_dir: bool) -> None:
        """Create a file at the given path, optionally creating the directory.

        Args:
            path (str): The path to the file.
            create_dir (bool): Whether to create the directory if it doesn't exist.

        Raises:
            JamStorageCreateError: If the file or directory could not be created.
        """
        if create_dir:
            base_dir = os.path.dirname(path)
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)
        with open(path, "a"):
            pass

        self._logger.debug(f"File {path} created")

    def close(self):
        """Close the file hook."""
        self.__hook.close()

    def get(self, name: str) -> dict[str, Any] | None:
        """Get a key by name.

        Args:
            name (str): The name of the key.

        Returns:
            dict[str, Any] | None: The value of the key, or None if not found.
        """
        self.__hook.seek(0, os.SEEK_END)
        size = self.__hook.tell()
        if not size:
            self._logger.debug(f"File {self.path} is empty")
            return None
        else:
            self.__hook.seek(0)
            return self._seralizer.loads(self.__hook)

    def store(self, name: str, data: dict[str, Any]) -> None:
        """Store a key with the given name and data.

        Args:
            name (str): The name of the key.
            data (dict[str, Any]): The data to store.
        """
        self.__hook.seek(0)
        self.__hook.write(self._seralizer.dumps(data).decode())
        self.__hook.flush()
        self._logger.debug(f"Key {name} stored in {self.path}")

    def delete(self, name: str) -> None:
        """Delete a key by name.

        Args:
            name (str): The name of the key.
        """
        self.__hook.seek(0)
        keys = self._seralizer.loads(self.__hook)
        if name in keys:
            del keys[name]
            self.__hook.seek(0)
            self.__hook.truncate()
            self.__hook.write(self._seralizer.dumps(keys))
            self.__hook.flush()
            self._logger.debug(f"Key {name} deleted from {self.path}")
        else:
            self._logger.debug(f"Key {name} not found in {self.path}")
