# -*- coding: utf-8 -*-

from __future__ import annotations

import base64
import zlib

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from jam.exceptions.saml import JamSAMLValidationError
from jam.saml.xml import SIG_RSA_SHA256


__all__ = [
    "encode_post",
    "decode_post",
    "encode_redirect",
    "decode_redirect",
    "build_redirect_url",
    "parse_redirect_request",
    "build_redirect_signature",
    "verify_redirect_signature",
]


def encode_post(xml_str: str) -> str:
    """Base64-encode SAML XML for HTTP-POST binding."""
    return base64.b64encode(xml_str.encode("utf-8")).decode("ascii")


def decode_post(b64_str: str) -> str:
    """Decode Base64-encoded SAML data from HTTP-POST binding."""
    return base64.b64decode(b64_str).decode("utf-8")


def _deflate(data: bytes) -> bytes:
    compress = zlib.compressobj(level=9, wbits=-zlib.MAX_WBITS)
    return compress.compress(data) + compress.flush()


def _inflate(data: bytes) -> bytes:
    decompress = zlib.decompressobj(wbits=-zlib.MAX_WBITS)
    return decompress.decompress(data) + decompress.flush()


def encode_redirect(xml_str: str) -> str:
    """Deflate + Base64-encode SAML XML for HTTP-Redirect binding."""
    return base64.b64encode(_deflate(xml_str.encode("utf-8"))).decode("ascii")


def decode_redirect(encoded: str) -> str:
    """Decode Deflate + Base64 SAML data from HTTP-Redirect binding."""
    return _inflate(base64.b64decode(encoded)).decode("utf-8")


def build_redirect_signature(
    signed_query: str,
    key: rsa.RSAPrivateKey,
) -> str:
    """Sign a query string for HTTP-Redirect binding with RSA-SHA256.

    Args:
        signed_query: Raw query string (SAMLRequest=SigAlg=...).
        key: RSA private key.

    Returns:
        Base64-encoded signature.
    """
    sig_bytes = key.sign(
        signed_query.encode("utf-8"),
        padding.PKCS1v15(),
        hashes.SHA256(),
    )
    return base64.b64encode(sig_bytes).decode("ascii")


def verify_redirect_signature(
    signed_query: str,
    signature_b64: str,
    key: rsa.RSAPublicKey,
) -> bool:
    """Verify an HTTP-Redirect binding signature.

    Args:
        signed_query: Raw query string that was signed.
        signature_b64: Base64-encoded signature.
        key: RSA public key.

    Returns:
        True if signature is valid.

    Raises:
        JamSAMLValidationError: If signature is invalid.
    """
    from cryptography.exceptions import InvalidSignature

    sig_bytes = base64.b64decode(signature_b64)
    try:
        key.verify(
            sig_bytes,
            signed_query.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
    except InvalidSignature:
        raise JamSAMLValidationError(
            message="Redirect binding signature is invalid.",
        )
    return True


def build_redirect_url(
    base_url: str,
    saml_params: dict[str, str],
    signing_key: rsa.RSAPrivateKey | None = None,
) -> str:
    """Build a signed redirect URL for HTTP-Redirect binding.

    Args:
        base_url: IdP SSO endpoint URL.
        saml_params: Query params (SAMLRequest, RelayState, etc.).
        signing_key: RSA private key for signing (optional).

    Returns:
        Full redirect URL with query string.
    """
    from urllib.parse import urlencode

    params = dict(saml_params)

    if signing_key is not None:
        params["SigAlg"] = SIG_RSA_SHA256
        query_string = urlencode(sorted(params.items()))
        sig = build_redirect_signature(query_string, signing_key)
        params["Signature"] = sig

    return f"{base_url}?{urlencode(params)}"


def parse_redirect_request(
    query_string: str,
    verify_key: rsa.RSAPublicKey | None = None,
) -> tuple[str, str]:
    """Parse a SAML redirect binding query string.

    Args:
        query_string: The raw query string from the redirect URL.
        verify_key: RSA public key to verify signature (optional).

    Returns:
        Tuple of (decoded SAML XML string, RelayState).

    Raises:
        JamSAMLValidationError: If signature verification fails.
    """
    from urllib.parse import parse_qs, urlencode

    params = parse_qs(query_string)

    saml_request = params.get("SAMLRequest", [None])[0]
    if saml_request is None:
        saml_response = params.get("SAMLResponse", [None])[0]
        if saml_response is None:
            raise JamSAMLValidationError(
                message="No SAMLRequest or SAMLResponse in redirect binding.",
            )
        saml_request = saml_response

    relay_state = params.get("RelayState", [None])[0]
    signature = params.get("Signature", [None])[0]
    sig_alg = params.get("SigAlg", [None])[0]

    if signature is not None and verify_key is not None:
        if sig_alg and sig_alg != SIG_RSA_SHA256:
            raise JamSAMLValidationError(
                message=f"Unsupported signature algorithm: {sig_alg}",
            )

        verify_params = {"SAMLRequest": saml_request}
        if relay_state:
            verify_params["RelayState"] = relay_state
        verify_params["SigAlg"] = sig_alg or SIG_RSA_SHA256
        signed_query = urlencode(sorted(verify_params.items()))
        verify_redirect_signature(signed_query, signature, verify_key)

    xml_str = decode_redirect(saml_request)
    return xml_str, relay_state or ""
