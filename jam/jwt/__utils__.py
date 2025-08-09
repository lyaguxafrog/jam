# -*- coding: utf-8 -*-

import base64


def __base64url_encode__(data: bytes) -> str:
    """Encodes data using URL-safe Base64 encoding.

    Removes padding characters ('=') typically added in standard Base64 encoding.

    Args:
        data (bytes): The data to encode.

    Returns:
        str: A URL-safe Base64 encoded string without padding.
    """
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def __base64url_decode__(data: str) -> bytes:
    """Decodes a URL-safe Base64 encoded string back to bytes.

    Automatically adds the necessary padding characters ('=') before decoding.

    Args:
        data (str): The Base64url encoded string to decode.

    Returns:
        bytes: The decoded byte data.
    """
    padding = "=" * ((4 - len(data) % 4) % 4)
    return base64.urlsafe_b64decode(data + padding)
