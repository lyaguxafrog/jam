# -*- coding: utf-8 -*-

from __future__ import annotations

import base64
import os
import xml.etree.ElementTree as ET

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from jam.exceptions.saml import JamSAMLValidationError
from jam.saml.xml import (
    ENC_AES256_GCM,
    ENC_ELEMENT,
    ENC_RSA_OAEP,
    NS_DS,
    NS_SAML,
    NS_XENC,
    canonicalize_xml,
    make_element,
    safe_fromstring,
    sub_element,
)


__all__ = [
    "encrypt_assertion",
    "decrypt_assertion",
    "encrypt_aes_key",
    "decrypt_aes_key",
    "load_encryption_key",
]


def load_encryption_key(pem: str) -> rsa.RSAPublicKey:
    """Load an RSA public key from PEM for encryption.

    Args:
        pem: PEM-encoded RSA public key or certificate.

    Returns:
        RSA public key.
    """
    from jam.saml.signature import load_public_key

    key = load_public_key(pem)
    if not isinstance(key, rsa.RSAPublicKey):
        raise JamSAMLValidationError(
            message="Encryption key must be an RSA public key.",
        )
    return key


def encrypt_aes_key(
    aes_key: bytes,
    public_key: rsa.RSAPublicKey,
) -> tuple[str, bytes]:
    """Encrypt an AES key with RSA-OAEP.

    Args:
        aes_key: 256-bit AES key bytes.
        public_key: RSA public key for encryption.

    Returns:
        Tuple of (base64-encoded ciphertext, OAEP padding used).
    """
    ct = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return base64.b64encode(ct).decode("ascii"), padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )


def decrypt_aes_key(
    encrypted_key_b64: str,
    private_key: rsa.RSAPrivateKey,
) -> bytes:
    """Decrypt an RSA-OAEP encrypted AES key.

    Args:
        encrypted_key_b64: Base64-encoded encrypted AES key.
        private_key: RSA private key for decryption.

    Returns:
        Decrypted 256-bit AES key bytes.
    """
    ct = base64.b64decode(encrypted_key_b64)
    return private_key.decrypt(
        ct,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def encrypt_assertion(
    assertion_elem: ET.Element,
    public_key: rsa.RSAPublicKey,
) -> ET.Element:
    """Encrypt a SAML Assertion element into an EncryptedAssertion.

    Generates a random AES-256-GCM key, encrypts the canonicalized
    assertion XML with it, then wraps the AES key with RSA-OAEP.

    Args:
        assertion_elem: The ``<saml:Assertion>`` element to encrypt.
        public_key: Recipient's RSA public key.

    Returns:
        ``<saml:EncryptedAssertion>`` element.
    """
    aes_key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    canonical = canonicalize_xml(assertion_elem)
    aesgcm = AESGCM(aes_key)
    ciphertext = aesgcm.encrypt(nonce, canonical, None)

    payload_b64 = base64.b64encode(nonce + ciphertext).decode("ascii")

    encrypted_key_b64, _ = encrypt_aes_key(aes_key, public_key)

    enc_assertion = make_element("EncryptedAssertion", NS_SAML)

    enc_data = make_element("EncryptedData", NS_XENC)
    enc_data.set("Type", ENC_ELEMENT)
    enc_assertion.append(enc_data)

    sub_element(
        enc_data,
        "EncryptionMethod",
        NS_XENC,
        attrib={"Algorithm": ENC_AES256_GCM},
    )

    key_info = make_element("KeyInfo", NS_DS)
    enc_data.append(key_info)

    enc_key = make_element("EncryptedKey", NS_XENC)
    key_info.append(enc_key)

    sub_element(
        enc_key,
        "EncryptionMethod",
        NS_XENC,
        attrib={"Algorithm": ENC_RSA_OAEP},
    )

    ciph_data = make_element("CipherData", NS_XENC)
    enc_key.append(ciph_data)
    sub_element(ciph_data, "CipherValue", NS_XENC, text=encrypted_key_b64)

    ciph_data2 = make_element("CipherData", NS_XENC)
    enc_data.append(ciph_data2)
    sub_element(ciph_data2, "CipherValue", NS_XENC, text=payload_b64)

    return enc_assertion


def decrypt_assertion(
    enc_assertion_elem: ET.Element,
    private_key: rsa.RSAPrivateKey,
) -> ET.Element:
    """Decrypt a ``<saml:EncryptedAssertion>`` element.

    Extracts the RSA-OAEP wrapped AES key, decrypts it, then
    decrypts the assertion XML payload.

    Args:
        enc_assertion_elem: The ``<saml:EncryptedAssertion>`` element.
        private_key: Recipient's RSA private key.

    Returns:
        Decrypted ``<saml:Assertion>`` element.

    Raises:
        JamSAMLValidationError: If decryption fails or structure is invalid.
    """
    enc_data = enc_assertion_elem.find(f"{{{NS_XENC}}}EncryptedData")
    if enc_data is None:
        raise JamSAMLValidationError(
            message="Missing EncryptedData in EncryptedAssertion.",
        )

    key_info = enc_data.find(f"{{{NS_DS}}}KeyInfo")
    if key_info is None:
        raise JamSAMLValidationError(
            message="Missing KeyInfo in EncryptedData.",
        )
    enc_key = key_info.find(f"{{{NS_XENC}}}EncryptedKey")
    if enc_key is None:
        raise JamSAMLValidationError(
            message="Missing EncryptedKey in KeyInfo.",
        )

    cipher_data_key = enc_key.find(f"{{{NS_XENC}}}CipherData")
    if cipher_data_key is None:
        raise JamSAMLValidationError(
            message="Missing CipherData in EncryptedKey.",
        )
    cipher_value_key = cipher_data_key.find(f"{{{NS_XENC}}}CipherValue")
    if cipher_value_key is None or not cipher_value_key.text:
        raise JamSAMLValidationError(
            message="Missing CipherValue in EncryptedKey.",
        )

    cipher_data = enc_data.find(f"{{{NS_XENC}}}CipherData")
    if cipher_data is None:
        raise JamSAMLValidationError(
            message="Missing CipherData in EncryptedData.",
        )
    cipher_value = cipher_data.find(f"{{{NS_XENC}}}CipherValue")
    if cipher_value is None or not cipher_value.text:
        raise JamSAMLValidationError(
            message="Missing CipherValue in EncryptedData.",
        )

    aes_key = decrypt_aes_key(cipher_value_key.text, private_key)

    raw = base64.b64decode(cipher_value.text)
    nonce = raw[:12]
    ct = raw[12:]

    aesgcm = AESGCM(aes_key)
    try:
        plaintext = aesgcm.decrypt(nonce, ct, None)
    except Exception as exc:
        raise JamSAMLValidationError(
            message=f"Failed to decrypt assertion: {exc}",
        ) from exc

    try:
        return safe_fromstring(plaintext.decode("utf-8"))
    except Exception as exc:
        raise JamSAMLValidationError(
            message=f"Decrypted assertion is not valid XML: {exc}",
        ) from exc
