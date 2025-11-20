# -*- coding: utf-8 -*-

import base64


def basic_auth_encode(login: str, password: str) -> str:
    """Encodes the login and password in a basic auth token.

    Args:
        login (str): Login
        password (str): Password

    Example:
        ```python
        >>> header = basic_auth_encode("admin", "qwerty1234")
        >>> print(header)
        YWRtaW46cXdlcnR5MTIzNA==
        ```
    """
    credentials = f"{login}:{password}"
    return base64.b64encode(credentials.encode()).decode()


def basic_auth_decode(data: str) -> tuple[str, str]:
    """Decodes basic auth token to login and password.

    Args:
        data (str): Decoded data

    Raises:
        ValueError: If incorrect format

    Example:
        >>> login, password = basic_auth_decode(header)
        >>> print(login, password)
        admin qwerty1234
    """
    decoded_bytes = base64.b64decode(data)
    decoded_str = decoded_bytes.decode()

    if ":" not in decoded_str:
        raise ValueError(
            "Incorrect format: no colon ‘:’ between username and password"
        )

    login, password = decoded_str.split(":", 1)
    return login, password
