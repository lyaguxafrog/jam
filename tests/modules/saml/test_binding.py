# -*- coding: utf-8 -*-

import pytest

from jam.saml.binding import (
    build_redirect_signature,
    build_redirect_url,
    decode_post,
    decode_redirect,
    encode_post,
    encode_redirect,
    parse_redirect_request,
    verify_redirect_signature,
)
from jam.saml.signature import load_private_key, load_public_key


SAMPLE_XML = '<?xml version="1.0"?><root><data>test</data></root>'


class TestPostBinding:
    def test_roundtrip(self):
        encoded = encode_post(SAMPLE_XML)
        assert isinstance(encoded, str)
        decoded = decode_post(encoded)
        assert decoded == SAMPLE_XML

    def test_not_equal_to_input(self):
        encoded = encode_post(SAMPLE_XML)
        assert encoded != SAMPLE_XML


class TestRedirectBinding:
    def test_encode_decode(self):
        encoded = encode_redirect(SAMPLE_XML)
        assert isinstance(encoded, str)
        decoded = decode_redirect(encoded)
        assert decoded == SAMPLE_XML

    def test_differs_from_post(self):
        assert encode_redirect(SAMPLE_XML) != encode_post(SAMPLE_XML)


class TestRedirectSignature:
    def test_sign_and_verify(self, private_key_pem, public_key_pem):
        key = load_private_key(private_key_pem)
        pub = load_public_key(public_key_pem)

        query = "SAMLRequest=abc123&SigAlg=rsa-sha256"
        sig = build_redirect_signature(query, key)

        assert verify_redirect_signature(query, sig, pub) is True

    def test_fails_on_tampered(self, private_key_pem, public_key_pem):
        key = load_private_key(private_key_pem)
        pub = load_public_key(public_key_pem)

        query = "SAMLRequest=abc123&SigAlg=rsa-sha256"
        sig = build_redirect_signature(query, key)

        from jam.exceptions.saml import JamSAMLValidationError

        with pytest.raises(JamSAMLValidationError):
            verify_redirect_signature(
                "SAMLRequest=tampered&SigAlg=rsa-sha256", sig, pub
            )


class TestRedirectUrl:
    def test_build_url_without_signing(self):
        url = build_redirect_url(
            "https://idp.example.com/sso",
            {"SAMLRequest": "abc"},
        )
        assert url.startswith("https://idp.example.com/sso?")
        assert "SAMLRequest=abc" in url

    def test_build_url_with_signing(self, private_key_pem):
        key = load_private_key(private_key_pem)
        url = build_redirect_url(
            "https://idp.example.com/sso",
            {"SAMLRequest": "abc", "RelayState": "relay"},
            signing_key=key,
        )
        assert "SigAlg=" in url
        assert "Signature=" in url


class TestParseRedirectRequest:
    def test_parse_without_verification(self):
        from urllib.parse import urlencode

        saml_encoded = encode_redirect(SAMPLE_XML)
        query = urlencode({"SAMLRequest": saml_encoded, "RelayState": "relay"})
        xml_str, relay = parse_redirect_request(query)
        assert xml_str == SAMPLE_XML
        assert relay == "relay"
