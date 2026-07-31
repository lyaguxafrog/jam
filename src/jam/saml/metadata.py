# -*- coding: utf-8 -*-

from __future__ import annotations

import xml.etree.ElementTree as ET

from jam.saml.types import SAMLMetadata
from jam.saml.xml import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
    NS_DS,
    NS_MD,
    make_element,
    register_namespaces,
)


__all__ = [
    "generate_idp_metadata",
    "generate_sp_metadata",
    "parse_metadata",
]


def _cert_to_keyinfo(cert_pem: str | None) -> ET.Element | None:
    if not cert_pem:
        return None
    key_info = make_element("KeyInfo", NS_DS)
    x509_data = make_element("X509Data", NS_DS)
    key_info.append(x509_data)
    x509_cert = make_element("X509Certificate", NS_DS)
    x509_data.append(x509_cert)
    lines = cert_pem.strip().split("\n")
    x509_cert.text = "".join(
        line.strip() for line in lines if not line.startswith("-----")
    )
    return key_info


def generate_idp_metadata(
    entity_id: str,
    sso_url: str,
    certificate: str | None = None,
    want_authn_requests_signed: bool = False,
) -> str:
    """Generate SAML IdP metadata XML.

    Args:
        entity_id: IdP entity ID.
        sso_url: Single Sign-On endpoint URL.
        certificate: PEM certificate string (included in KeyDescriptor).
        want_authn_requests_signed: Whether IdP requires signed AuthnRequests.

    Returns:
        SAML metadata XML string.
    """
    register_namespaces()

    entity = make_element("EntityDescriptor", NS_MD)
    entity.set("entityID", entity_id)

    idp_sso = make_element("IDPSSODescriptor", NS_MD)
    idp_sso.set(
        "protocolSupportEnumeration",
        "urn:oasis:names:tc:SAML:2.0:protocol",
    )
    entity.append(idp_sso)

    if want_authn_requests_signed:
        idp_sso.set("WantAuthnRequestsSigned", "true")

    ki = _cert_to_keyinfo(certificate)
    if ki is not None:
        kd = make_element("KeyDescriptor", NS_MD)
        kd.set("use", "signing")
        kd.append(ki)
        idp_sso.append(kd)

    for binding in (BINDING_HTTP_REDIRECT, BINDING_HTTP_POST):
        sso = make_element("SingleSignOnService", NS_MD)
        sso.set("Binding", binding)
        sso.set("Location", sso_url)
        idp_sso.append(sso)

    return ET.tostring(entity, encoding="unicode")


def generate_sp_metadata(
    entity_id: str,
    acs_url: str,
    certificate: str | None = None,
    authn_requests_signed: bool = False,
) -> str:
    """Generate SAML SP metadata XML.

    Args:
        entity_id: SP entity ID.
        acs_url: Assertion Consumer Service URL.
        certificate: PEM certificate string (included in KeyDescriptor).
        authn_requests_signed: Whether SP signs AuthnRequests.

    Returns:
        SAML metadata XML string.
    """
    register_namespaces()

    entity = make_element("EntityDescriptor", NS_MD)
    entity.set("entityID", entity_id)

    sp_sso = make_element("SPSSODescriptor", NS_MD)
    sp_sso.set(
        "protocolSupportEnumeration",
        "urn:oasis:names:tc:SAML:2.0:protocol",
    )
    entity.append(sp_sso)

    if authn_requests_signed:
        sp_sso.set("AuthnRequestsSigned", "true")

    ki = _cert_to_keyinfo(certificate)
    if ki is not None:
        kd = make_element("KeyDescriptor", NS_MD)
        kd.set("use", "signing")
        kd.append(ki)
        sp_sso.append(kd)

    acs = make_element("AssertionConsumerService", NS_MD)
    acs.set("Binding", BINDING_HTTP_POST)
    acs.set("Location", acs_url)
    acs.set("index", "0")
    sp_sso.append(acs)

    return ET.tostring(entity, encoding="unicode")


def parse_metadata(metadata_xml: str) -> SAMLMetadata:
    """Parse SAML 2.0 metadata XML.

    Args:
        metadata_xml: Raw metadata XML string.

    Returns:
        SAMLMetadata with entity_id, role, endpoints, and certificate.

    Raises:
        ValueError: If neither IdP nor SP descriptor is found.
    """
    root = ET.fromstring(metadata_xml)
    entity_id = root.get("entityID", "")

    idp_sso = root.find(f"{{{NS_MD}}}IDPSSODescriptor")
    sp_sso = root.find(f"{{{NS_MD}}}SPSSODescriptor")

    if idp_sso is not None:
        role = "idp"
        sso = idp_sso.find(f"{{{NS_MD}}}SingleSignOnService")
        sso_url = sso.get("Location") if sso is not None else None
        want_signed = (
            idp_sso.get("WantAuthnRequestsSigned", "false").lower() == "true"
        )

        cert = _extract_cert(idp_sso)
        return SAMLMetadata(
            entity_id=entity_id,
            role=role,
            sso_url=sso_url,
            certificate=cert,
            want_authn_requests_signed=want_signed,
        )

    if sp_sso is not None:
        role = "sp"
        acs = sp_sso.find(f"{{{NS_MD}}}AssertionConsumerService")
        acs_url = acs.get("Location") if acs is not None else None
        authn_signed = (
            sp_sso.get("AuthnRequestsSigned", "false").lower() == "true"
        )

        cert = _extract_cert(sp_sso)
        return SAMLMetadata(
            entity_id=entity_id,
            role=role,
            acs_url=acs_url,
            certificate=cert,
            authn_requests_signed=authn_signed,
        )

    raise ValueError(
        "Unknown SAML metadata type: no IDPSSODescriptor or SPSSODescriptor found."
    )


def _extract_cert(parent: ET.Element) -> str | None:
    kd = parent.find(f"{{{NS_MD}}}KeyDescriptor")
    if kd is None:
        return None
    ki = kd.find(f"{{{NS_DS}}}KeyInfo")
    if ki is None:
        return None
    x509_data = ki.find(f"{{{NS_DS}}}X509Data")
    if x509_data is None:
        return None
    x509_cert = x509_data.find(f"{{{NS_DS}}}X509Certificate")
    if x509_cert is None or not x509_cert.text:
        return None
    b64 = x509_cert.text.strip()
    return (
        "-----BEGIN CERTIFICATE-----\n"
        + "\n".join(b64[i : i + 64] for i in range(0, len(b64), 64))
        + "\n-----END CERTIFICATE-----"
    )
