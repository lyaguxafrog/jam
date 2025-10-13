# -*- coding: utf-8 -*-


def xor_my_data(data: str, key: str) -> str:
    """Encrypts a string using a secret key with the XOR cipher.

    This function performs an XOR operation on each byte of the input data
    with the corresponding byte of the key. If the key is shorter than the
    data, it wraps around and continues from the beginning of the key.
    If you need to decrypt data, use the same function
    with the same secret key. XOR is a symmetric operation.

    Args:
        data (str): The plain text string to be encrypted.
        key (str): The secret key used for encryption.

    Returns:
        str: The encrypted data represented as a hexadecimal string.

    Example:
        ```python
        >>> encrypted = xor_my_data("Hello, World!", "secretkey")
        >>> print(encrypted)
        <...encrypted hex string...>
        ```
    """
    data_bytes = data.encode("utf-8")
    key_bytes = key.encode("utf-8")

    encrypted_bytes = bytearray()
    for i in range(len(data_bytes)):
        encrypted_byte = data_bytes[i] ^ key_bytes[i % len(key_bytes)]
        encrypted_bytes.append(encrypted_byte)

    return encrypted_bytes.hex()
