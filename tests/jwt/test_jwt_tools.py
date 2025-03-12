# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import pytest

from jam.exceptions import (
    EmptyPublicKey,
    EmptySecretKey,
    EmtpyPrivateKey,
    TokenLifeTimeExpired,
)
from jam.jwt.__tools__ import __gen_jwt__, __validate_jwt__
from jam.utils import generate_rsa_key_pair


private_key = generate_rsa_key_pair().get("private")
public_key = generate_rsa_key_pair().get("public")
secret = "SUPER_SECRET"


# GEN JWT
def test_gen_jwt_hmac():
    header = {"alg": "HS256", "type": "jwt"}
    payload = {"id": 1}

    token = __gen_jwt__(header, payload, secret=secret)

    assert isinstance(token, str)
    assert len(token.split(".")) == 3  # JWT has three parts


def test_gen_jwt_rsa():
    header = {"alg": "RS256", "type": "jwt"}
    payload = {"id": 1}

    token = __gen_jwt__(header, payload, private_key=private_key)

    assert isinstance(token, str)
    assert len(token.split(".")) == 3  # JWT has three parts


def test_gen_jwt_hmac_missing_secret():
    header = {"alg": "HS256", "type": "jwt"}
    payload = {"id": 1}

    with pytest.raises(EmptySecretKey):
        __gen_jwt__(header, payload, secret=None)


def test_gen_jwt_rsa_missing_private_key():
    header = {"alg": "RS256", "type": "jwt"}
    payload = {"id": 1}

    with pytest.raises(EmtpyPrivateKey):
        __gen_jwt__(header, payload, private_key=None)


def test_gen_jwt_unsupported_algorithm():
    header = {"alg": "ES256", "type": "jwt"}
    payload = {"id": 1}

    with pytest.raises(ValueError, match="Unsupported algorithm"):
        __gen_jwt__(header, payload, secret=secret)


# VALIDATE
def test_validate_jwt_hmac():
    header = {"alg": "HS256", "type": "jwt"}
    payload = {
        "id": 1,
        "exp": (datetime.now() + timedelta(hours=1)).timestamp(),
    }

    token = __gen_jwt__(header, payload, secret=secret)

    validated_payload = __validate_jwt__(token, check_exp=True, secret=secret)

    assert validated_payload == payload


def test_validate_jwt_rsa():
    keys = generate_rsa_key_pair()
    private_key = keys["private"]
    public_key = keys["public"]

    header = {"alg": "RS256", "type": "jwt"}
    payload = {
        "id": 1,
        "exp": (datetime.now() + timedelta(hours=1)).timestamp(),
    }

    token = __gen_jwt__(header, payload, private_key=private_key)

    validated_payload = __validate_jwt__(
        token, check_exp=True, public_key=public_key
    )

    assert validated_payload == payload


def test_validate_jwt_hmac_invalid_signature():
    header = {"alg": "HS256", "type": "jwt"}
    payload = {
        "id": 1,
        "exp": (datetime.now() + timedelta(hours=1)).timestamp(),
    }

    token = __gen_jwt__(header, payload, secret=secret)

    # Tamper with the token
    tampered_token = token[:-1] + "X"  # Change the last character

    with pytest.raises(ValueError, match="Invalid token signature"):
        __validate_jwt__(tampered_token, check_exp=True, secret=secret)


def test_validate_jwt_rsa_invalid_signature():
    header = {"alg": "RS256", "type": "jwt"}
    payload = {
        "id": 1,
        "exp": (datetime.now() + timedelta(hours=1)).timestamp(),
    }

    token = __gen_jwt__(header, payload, private_key=private_key)

    # Tamper with the token
    tampered_token = token[:-1] + "X"  # Change the last character

    with pytest.raises(ValueError, match="Invalid signature"):
        __validate_jwt__(tampered_token, check_exp=True, public_key=public_key)


def test_validate_jwt_hmac_missing_secret():
    header = {"alg": "HS256", "type": "jwt"}
    payload = {
        "id": 1,
        "exp": (datetime.now() + timedelta(hours=1)).timestamp(),
    }

    token = __gen_jwt__(header, payload, secret=secret)

    with pytest.raises(EmptySecretKey):
        __validate_jwt__(token, check_exp=True, secret=None)


def test_validate_jwt_rsa_missing_public_key():
    header = {"alg": "RS256", "type": "jwt"}
    payload = {
        "id": 1,
        "exp": (datetime.now() + timedelta(hours=1)).timestamp(),
    }

    token = __gen_jwt__(header, payload, private_key=private_key)

    with pytest.raises(EmptyPublicKey):
        __validate_jwt__(token, check_exp=True, public_key=None)


def test_validate_jwt_expired_token():
    header = {"alg": "HS256", "type": "jwt"}
    payload = {
        "id": 1,
        "exp": (datetime.now() - timedelta(seconds=1)).timestamp(),
    }  # Expired token

    token = __gen_jwt__(header, payload, secret=secret)

    with pytest.raises(TokenLifeTimeExpired):
        __validate_jwt__(token, check_exp=True, secret=secret)
