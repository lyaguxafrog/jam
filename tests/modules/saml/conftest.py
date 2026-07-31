# -*- coding: utf-8 -*-

import pytest

from jam.utils.rsa import generate_rsa_key_pair


@pytest.fixture()
def key_pair() -> dict[str, str]:
    return generate_rsa_key_pair(2048)


@pytest.fixture()
def private_key_pem(key_pair) -> str:
    return key_pair["private"]


@pytest.fixture()
def public_key_pem(key_pair) -> str:
    return key_pair["public"]


@pytest.fixture()
def cert_pem(key_pair) -> str:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID
    import datetime

    private = serialization.load_pem_private_key(
        key_pair["private"].encode("utf-8"), password=None
    )
    assert isinstance(private, rsa.RSAPrivateKey)
    public = private.public_key()

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "test"),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(public)
        .serial_number(1)
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1))
        .sign(private, hashes.SHA256())
    )
    return cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
