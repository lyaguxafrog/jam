# -*- coding: utf-8 -*-

import pytest

from jam.jwt.module import JWT
from jam.utils import generate_rsa_key_pair, generate_ecdsa_p384_keypair


@pytest.fixture()
def symmetric_key() -> str:
    return "SOME_JWT_KEY"

@pytest.fixture()
def rsa_key_pair() -> dict[str, str]:
    return generate_rsa_key_pair()

@pytest.fixture()
def ecdsa_key_pair() -> dict[str, str]:
    return generate_ecdsa_p384_keypair()


@pytest.fixture
def jwt_hs(symmetric_key):
    return JWT(
        alg="HS256",
        secret=symmetric_key,
    )

@pytest.fixture
def jwt_rsa(rsa_key_pair):
    return JWT(
        alg="RS256",
        secret=rsa_key_pair["private"],
    )

@pytest.fixture()
def jwt_ecdsa(ecdsa_key_pair):
    return JWT(
        alg="ES256",
        secret=ecdsa_key_pair["private"],
    )

def test_jwt_hs_encode(jwt_hs):
	payload = {"user_id": 123}
	token = jwt_hs.encode(payload)
	assert token is not None
	assert isinstance(token, str)
	assert token.startswith("ey")
	assert token.count(".") == 2


def test_jwt_hs_decode(jwt_hs):
	payload = {"user_id": 123}
	token = jwt_hs.encode(payload)
	decoded_payload = jwt_hs.decode(token)
	assert decoded_payload == payload


def test_jwt_rsa_encode(jwt_rsa):
	payload = {"user_id": 123}
	token = jwt_rsa.encode(payload)
	assert token is not None
	assert isinstance(token, str)
	assert token.startswith("ey")
	assert token.count(".") == 2


def test_jwt_rsa_decode(jwt_rsa, rsa_key_pair):
	payload = {"user_id": 123}
	token = jwt_rsa.encode(payload)
	decoded_payload = jwt_rsa.decode(token)
	assert decoded_payload == payload

	# decode with public key
	decoded_payload = jwt_rsa.decode(token, rsa_key_pair["public"])
	assert decoded_payload == payload

def test_jwt_ecdsa_encode(jwt_ecdsa):
	payload = {"user_id": 123}
	token = jwt_ecdsa.encode(payload)
	assert token is not None
	assert isinstance(token, str)
	assert token.startswith("ey")
	assert token.count(".") == 2


def test_jwt_ecdsa_decode(jwt_ecdsa, ecdsa_key_pair):
	payload = {"user_id": 123}
	token = jwt_ecdsa.encode(payload)
	decoded_payload = jwt_ecdsa.decode(token)
	assert decoded_payload == payload

	# decode with public key
	decoded_payload = jwt_ecdsa.decode(token, ecdsa_key_pair["public"])
	assert decoded_payload == payload
