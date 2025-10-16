# -*- coding: utf-8 -*-

import json
from typing import Any, Union


try:
    import msgspec
except ImportError:
    pass

from jam.__abc_encoder__ import BaseEncoder


class JsonEncoder(BaseEncoder):
    """Json encoder."""

    @classmethod
    def dumps(cls, var: dict[str, Any]) -> bytes:
        """Dump dict."""
        return json.dumps(var, sort_keys=True, separators=(",", ":")).encode(
            "utf8"
        )

    @classmethod
    def loads(cls, var: Union[str, bytes]) -> dict[str, Any]:
        """Load json."""
        return json.loads(var)


class MsgspecJsonEncoder(BaseEncoder):
    """JSON encoder based on msgspec.

    To use it, you need to install the optional msgspec: `pip install msgspec`
    """

    @classmethod
    def dumps(cls, var: dict[str, Any]) -> bytes:
        """Dump dict."""
        return msgspec.json.encode(var)

    @classmethod
    def loads(cls, var: Union[str, bytes]) -> dict[str, Any]:
        """Load JSON to dict."""
        return msgspec.json.decode(
            var if isinstance(var, bytes) else var.encode("utf-8")
        )
