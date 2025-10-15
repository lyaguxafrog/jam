# -*- coding: utf-8 -*-

import base64


def __b64url_nopad__(b: bytes) -> str:
    """Return B64 nopad."""
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")
