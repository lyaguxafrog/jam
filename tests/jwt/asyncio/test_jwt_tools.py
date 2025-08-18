# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import pytest

from jam.aio.jwt.tools import __gen_jwt_async__, __validate_jwt_async__
from jam.exceptions import (
    EmptyPublicKey,
    EmptySecretKey,
    EmtpyPrivateKey,
    TokenLifeTimeExpired,
)
from jam.jwt.__utils__ import __base64url_decode__, __base64url_encode__
from jam.utils import generate_rsa_key_pair


private_key = generate_rsa_key_pair().get("private")
public_key = generate_rsa_key_pair().get("public")
secret = "SUPER_SECRET"


# GEN JWT
@pytest.mark.asyncio
async def test_gen_jwt_hmac():
    header = {"alg": "HS256", "type": "jwt"}
    payload = {"id": 1}

    token = await __gen_jwt_async__(header, payload, secret=secret)

    assert isinstance(token, str)
    assert len(token.split(".")) == 3  # JWT has three parts


@pytest.mark.asyncio
async def test_gen_jwt_rsa():
    header = {"alg": "RS256", "type": "jwt"}
    payload = {"id": 1}

    token = await __gen_jwt_async__(header, payload, private_key=private_key)

    assert isinstance(token, str)
    assert len(token.split(".")) == 3  # JWT has three parts


@pytest.mark.asyncio
async def test_gen_jwt_hmac_missing_secret():
    header = {"alg": "HS256", "type": "jwt"}
    payload = {"id": 1}

    with pytest.raises(EmptySecretKey):
        await __gen_jwt_async__(header, payload, secret=None)


@pytest.mark.asyncio
async def test_gen_jwt_rsa_missing_private_key():
    header = {"alg": "RS256", "type": "jwt"}
    payload = {"id": 1}

    with pytest.raises(EmtpyPrivateKey):
        await __gen_jwt_async__(header, payload, private_key=None)


@pytest.mark.asyncio
async def test_gen_jwt_unsupported_algorithm():
    header = {"alg": "ES256", "type": "jwt"}
    payload = {"id": 1}

    with pytest.raises(ValueError, match="Unsupported algorithm"):
        await __gen_jwt_async__(header, payload, secret=secret)


# VALIDATE
@pytest.mark.asyncio
async def test_validate_jwt_hmac():
    header = {"alg": "HS256", "type": "jwt"}
    payload = {
        "id": 1,
        "exp": (datetime.now() + timedelta(hours=1)).timestamp(),
    }

    token = await __gen_jwt_async__(header, payload, secret=secret)

    validated_payload = await __validate_jwt_async__(
        token, check_exp=True, secret=secret
    )

    assert validated_payload == payload


@pytest.mark.asyncio
async def test_validate_jwt_rsa():
    keys = generate_rsa_key_pair()
    private_key = keys["private"]
    public_key = keys["public"]

    header = {"alg": "RS256", "type": "jwt"}
    payload = {
        "id": 1,
        "exp": (datetime.now() + timedelta(hours=1)).timestamp(),
    }

    token = await __gen_jwt_async__(header, payload, private_key=private_key)

    validated_payload = await __validate_jwt_async__(
        token, check_exp=True, public_key=public_key
    )

    assert validated_payload == payload


@pytest.mark.asyncio
async def test_validate_jwt_hmac_invalid_signature():
    header = {"alg": "HS256", "type": "jwt"}
    payload = {
        "id": 1,
        "exp": (datetime.now() + timedelta(hours=1)).timestamp(),
    }

    token = await __gen_jwt_async__(header, payload, secret=secret)

    # Tamper with the token
    parts = token.split(".")
    sig_bytes = bytearray(
        __base64url_decode__(parts[2])
    )  # Decode the signature part
    sig_bytes[0] ^= 0xFF  # Flip the first byte to tamper with the signature
    parts[2] = __base64url_encode__(
        bytes(sig_bytes)
    )  # Re-encode the tampered signature
    tampered_token = ".".join(parts)

    with pytest.raises(ValueError, match="Invalid token signature"):
        await __validate_jwt_async__(
            tampered_token, check_exp=True, secret=secret
        )


@pytest.mark.asyncio
async def test_validate_jwt_rsa_invalid_signature():
    header = {"alg": "RS256", "type": "jwt"}
    payload = {
        "id": 1,
        "exp": (datetime.now() + timedelta(hours=1)).timestamp(),
    }

    token = await __gen_jwt_async__(header, payload, private_key=private_key)

    # Tamper with the token
    tampered_token = token[:-1] + "X"  # Change the last character

    with pytest.raises(ValueError, match="Invalid signature"):
        await __validate_jwt_async__(
            tampered_token, check_exp=True, public_key=public_key
        )


@pytest.mark.asyncio
async def test_validate_jwt_hmac_missing_secret():
    header = {"alg": "HS256", "type": "jwt"}
    payload = {
        "id": 1,
        "exp": (datetime.now() + timedelta(hours=1)).timestamp(),
    }

    token = await __gen_jwt_async__(header, payload, secret=secret)

    with pytest.raises(EmptySecretKey):
        await __validate_jwt_async__(token, check_exp=True, secret=None)


@pytest.mark.asyncio
async def test_validate_jwt_rsa_missing_public_key():
    header = {"alg": "RS256", "type": "jwt"}
    payload = {
        "id": 1,
        "exp": (datetime.now() + timedelta(hours=1)).timestamp(),
    }

    token = await __gen_jwt_async__(header, payload, private_key=private_key)

    with pytest.raises(EmptyPublicKey):
        await __validate_jwt_async__(token, check_exp=True, public_key=None)


@pytest.mark.asyncio
async def test_validate_jwt_expired_token():
    header = {"alg": "HS256", "type": "jwt"}
    payload = {
        "id": 1,
        "exp": (datetime.now() - timedelta(seconds=1)).timestamp(),
    }  # Expired token

    token = await __gen_jwt_async__(header, payload, secret=secret)

    with pytest.raises(TokenLifeTimeExpired):
        await __validate_jwt_async__(token, check_exp=True, secret=secret)
