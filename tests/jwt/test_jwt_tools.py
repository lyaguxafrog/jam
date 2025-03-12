# -*- coding: utf-8 -*-

import pytest

from jam.exceptions import EmptySecretKey, EmtpyPrivateKey
from jam.jwt.__tools__ import __gen_jwt__
from jam.utils import generate_rsa_key_pair


private_key = generate_rsa_key_pair().get("private")
secret = "SUPER_SECRET"


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
