# -*- coding: utf-8 -*-

import pytest
from jam.jose import JWK, JWKSet


class TestJWKOct:
    def test_create_from_dict(self):
        jwk = JWK.from_dict({"kty": "oct", "k": "SGVsbG9Xb3JsZA"})
        assert jwk.kty == "oct"
        assert jwk.alg is None
        assert jwk.kid is None

    def test_create_with_optional_params(self):
        jwk = JWK.from_dict(
            {
                "kty": "oct",
                "k": "SGVsbG9Xb3JsZA",
                "alg": "HS256",
                "kid": "my-key",
                "use": "sig",
            }
        )
        assert jwk.alg == "HS256"
        assert jwk.kid == "my-key"

    def test_sign_and_verify(self):
        jwk = JWK.from_dict({"kty": "oct", "k": "SGVsbG9Xb3JsZA"})
        token = jwk.sign(b"test data", "HS256")
        assert token.count(".") == 2
        result = jwk.verify(token)
        assert result["header"]["alg"] == "HS256"
        assert result["payload"] == b"test data"

    def test_sign_with_default_alg(self):
        jwk = JWK.from_dict(
            {"kty": "oct", "k": "SGVsbG9Xb3JsZA", "alg": "HS256"}
        )
        token = jwk.sign(b"test data")
        result = jwk.verify(token)
        assert result["payload"] == b"test data"

    def test_to_dict(self):
        data = {"kty": "oct", "k": "SGVsbG9Xb3JsZA", "kid": "my-key"}
        jwk = JWK.from_dict(data)
        assert jwk.to_dict() == data


class TestJWKRSA:
    def test_create_from_pem(self):
        from jam.utils import generate_rsa_key_pair

        key_pair = generate_rsa_key_pair()

        jwk_data = {
            "kty": "RSA",
            "n": "wVXw",
            "e": "AQAB",
        }
        jwk = JWK.from_dict(jwk_data)
        assert jwk.kty == "RSA"

    def test_to_dict(self):
        from jam.utils import generate_rsa_key_pair

        key_pair = generate_rsa_key_pair()
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa

        private_key = serialization.load_pem_private_key(
            key_pair["private"].encode(),
            password=None,
        )
        public_key = private_key.public_key()
        public_numbers = public_key.public_numbers()

        n_bytes = public_numbers.n.to_bytes(
            (public_numbers.n.bit_length() + 7) // 8, "big"
        )
        e_bytes = public_numbers.e.to_bytes(
            (public_numbers.e.bit_length() + 7) // 8, "big"
        )

        from jam.jose.utils import __base64url_encode__

        jwk_data = {
            "kty": "RSA",
            "n": __base64url_encode__(n_bytes),
            "e": __base64url_encode__(e_bytes),
        }

        jwk = JWK.from_dict(jwk_data)
        assert jwk.to_dict() == jwk_data


class TestJWKEC:
    def test_create_p256(self):
        jwk = JWK.from_dict(
            {
                "kty": "EC",
                "crv": "P-256",
                "x": "WbbzO-PnZ4RwWdKQeFbK4xT5K3zL3tW0u4eF9kU2o",
                "y": "WbbzO-PnZ4RwWdKQeFbK4xT5K3zL3tW0u4eF9kU2o",
            }
        )
        assert jwk.kty == "EC"
        assert jwk.kid is None

    def test_create_p384(self):
        jwk = JWK.from_dict(
            {
                "kty": "EC",
                "crv": "P-384",
                "x": "WbbzO-PnZ4RwWdKQeFbK4xT5K3zL3tW0u4eF9kU2o",
                "y": "WbbzO-PnZ4RwWdKQeFbK4xT5K3zL3tW0u4eF9kU2o",
            }
        )
        assert jwk.kty == "EC"

    def test_create_p521(self):
        jwk = JWK.from_dict(
            {
                "kty": "EC",
                "crv": "P-521",
                "x": "WbbzO-PnZ4RwWdKQeFbK4xT5K3zL3tW0u4eF9kU2o",
                "y": "WbbzO-PnZ4RwWdKQeFbK4xT5K3zL3tW0u4eF9kU2o",
            }
        )
        assert jwk.kty == "EC"

    def test_create_with_optional_params(self):
        jwk = JWK.from_dict(
            {
                "kty": "EC",
                "crv": "P-256",
                "x": "WbbzO-PnZ4RwWdKQeFbK4xT5K3zL3tW0u4eF9kU2o",
                "y": "WbbzO-PnZ4RwWdKQeFbK4xT5K3zL3tW0u4eF9kU2o",
                "alg": "ES256",
                "kid": "ec-key-1",
                "use": "sig",
            }
        )
        assert jwk.alg == "ES256"
        assert jwk.kid == "ec-key-1"

    def test_sign_and_verify_es256(self):
        from jam.utils import generate_ecdsa_p384_keypair

        key_pair = generate_ecdsa_p384_keypair()

        from jam.jose.jwk import JWK

        jwk = JWK.from_dict(
            {"kty": "oct", "k": "U29tZVNlY3JldEtleUZvclRlc3Rpbmc"}
        )
        token = jwk.sign(b"test data", "HS256")
        result = jwk.verify(token)
        assert result["payload"] == b"test data"


class TestJWKValidationErrors:
    def test_missing_kty(self):
        with pytest.raises(Exception):
            JWK.from_dict({"k": "SGVsbG9Xb3JsZA"})

    def test_invalid_kty(self):
        with pytest.raises(Exception):
            JWK.from_dict({"kty": "UNKNOWN", "k": "SGVsbG9Xb3JsZA"})

    def test_rsa_missing_n(self):
        with pytest.raises(Exception):
            JWK.from_dict({"kty": "RSA", "e": "AQAB"})

    def test_rsa_missing_e(self):
        with pytest.raises(Exception):
            JWK.from_dict({"kty": "RSA", "n": "wVXw"})

    def test_ec_missing_crvs(self):
        with pytest.raises(Exception):
            JWK.from_dict({"kty": "EC", "x": "abc", "y": "def"})

    def test_ec_invalid_curve(self):
        with pytest.raises(Exception):
            JWK.from_dict(
                {
                    "kty": "EC",
                    "crv": "P-999",
                    "x": "abc",
                    "y": "def",
                }
            )

    def test_oct_missing_k(self):
        with pytest.raises(Exception):
            JWK.from_dict({"kty": "oct"})


class TestJWKSet:
    def test_create_empty(self):
        jwkset = JWKSet()
        assert jwkset.to_dict() == {"keys": []}

    def test_create_with_keys(self):
        keys = [
            {"kty": "oct", "k": "SGVsbG9Xb3JsZA", "kid": "key1"},
            {"kty": "RSA", "n": "wVXw", "e": "AQAB", "kid": "key2"},
        ]
        jwkset = JWKSet(keys=keys)
        assert len(jwkset.filter()) == 2

    def test_get_by_kid(self):
        keys = [
            {"kty": "oct", "k": "SGVsbG9Xb3JsZA", "kid": "key1"},
            {"kty": "oct", "k": "SGVsbG9Xb3JsZB", "kid": "key2"},
        ]
        jwkset = JWKSet(keys=keys)
        result = jwkset.get_by_kid("key2")
        assert result["kid"] == "key2"

    def test_get_by_kid_not_found(self):
        jwkset = JWKSet(
            keys=[{"kty": "oct", "k": "SGVsbG9Xb3JsZA", "kid": "key1"}]
        )
        result = jwkset.get_by_kid("nonexistent")
        assert result is None

    def test_get_by_kty(self):
        keys = [
            {"kty": "oct", "k": "SGVsbG9Xb3JsZA"},
            {"kty": "RSA", "n": "wVXw", "e": "AQAB"},
        ]
        jwkset = JWKSet(keys=keys)
        result = jwkset.get_by_kty("oct")
        assert len(result) == 1
        assert result[0]["kty"] == "oct"

    def test_filter_by_kty(self):
        keys = [
            {"kty": "oct", "k": "SGVsbG9Xb3JsZA"},
            {"kty": "RSA", "n": "wVXw", "e": "AQAB"},
            {"kty": "RSA", "n": "wVXx", "e": "AQAB"},
        ]
        jwkset = JWKSet(keys=keys)
        result = jwkset.filter(kty="RSA")
        assert len(result) == 2

    def test_filter_by_multiple_criteria(self):
        keys = [
            {"kty": "oct", "k": "SGVsbG9Xb3JsZA", "alg": "HS256"},
            {"kty": "oct", "k": "SGVsbG9Xb3JsZB", "alg": "HS384"},
        ]
        jwkset = JWKSet(keys=keys)
        result = jwkset.filter(kty="oct", alg="HS256")
        assert len(result) == 1
        assert result[0]["alg"] == "HS256"

    def test_to_dict(self):
        keys = [{"kty": "oct", "k": "SGVsbG9Xb3JsZA", "kid": "key1"}]
        jwkset = JWKSet(keys=keys)
        assert jwkset.to_dict() == {"keys": keys}

    def test_from_dict(self):
        data = {"keys": [{"kty": "oct", "k": "SGVsbG9Xb3JsZA"}]}
        jwkset = JWKSet.from_dict(data)
        assert len(jwkset.filter()) == 1
