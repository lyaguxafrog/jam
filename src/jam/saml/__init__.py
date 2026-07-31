# -*- coding: utf-8 -*-

"""Security Assertion Markup Language (SAML 2.0).

Supports both Service Provider and Identity Provider roles.
Zero external dependencies — built on stdlib xml + cryptography.
"""

from typing import Any

from jam.__deprecated__ import deprecated
from jam.saml.__base__ import BaseSAML
from jam.saml.saml import SAML
from jam.saml.types import (
    SAMLArtifactResolve,
    SAMLArtifactResponse,
    SAMLAssertion,
    SAMLAttributeQuery,
    SAMLAuthnStatement,
    SAMLConditions,
    SAMLLogoutRequest,
    SAMLLogoutResponse,
    SAMLManageNameIDRequest,
    SAMLManageNameIDResponse,
    SAMLMetadata,
    SAMLRequest,
    SAMLResponse,
    SAMLSubject,
)


@deprecated()
def create_instance(
    role: str = "sp",
    private_key: str | None = None,
    public_key: str | None = None,
    certificate: str | None = None,
    entity_id: str | None = None,
    acs_url: str | None = None,
    sso_url: str | None = None,
    idp_public_key: str | None = None,
    sp_public_key: str | None = None,
    encryption_key: str | None = None,
    default_exp: int = 300,
    allowed_clock_skew: int = 120,
    want_assertions_signed: bool = True,
    replay_ttl: int = 300,
    **kwargs: Any,
) -> SAML:
    """Create a SAML instance.

    Args:
        role: ``"sp"`` (Service Provider) or ``"idp"`` (Identity Provider).
        private_key: PEM string or path to private key file.
        public_key: PEM string or path to public key / certificate file.
        certificate: PEM string or path to certificate file (included in metadata/signature).
        entity_id: Entity ID of this SAML party.
        acs_url: Assertion Consumer Service URL (for SP role).
        sso_url: Single Sign-On URL (for IdP role).
        idp_public_key: IdP public key / certificate PEM (for SP — signature verification).
        sp_public_key: SP public key / certificate PEM (for IdP — SLO verification).
        encryption_key: SP public key PEM for assertion encryption (IdP).
        default_exp: Default assertion lifetime in seconds (default 300).
        allowed_clock_skew: Clock skew tolerance in seconds (default 120).
        want_assertions_signed: Require signed assertions (SP, default True).
        replay_ttl: Seconds before a consumed ID is eligible for cleanup (default 300).
        **kwargs: Additional parameters passed to the SAML constructor.

    Returns:
        SAML instance.
    """
    if kwargs.get("custom_module"):
        from jam.utils.config_maker import __module_loader__

        module_cls = __module_loader__(kwargs["custom_module"])
        return module_cls(
            role=role,
            private_key=private_key,
            public_key=public_key,
            certificate=certificate,
            entity_id=entity_id,
            acs_url=acs_url,
            sso_url=sso_url,
            idp_public_key=idp_public_key,
            sp_public_key=sp_public_key,
            encryption_key=encryption_key,
            default_exp=default_exp,
            allowed_clock_skew=allowed_clock_skew,
            want_assertions_signed=want_assertions_signed,
            replay_ttl=replay_ttl,
        )

    return SAML(
        role=role,
        private_key=private_key,
        public_key=public_key,
        certificate=certificate,
        entity_id=entity_id,
        acs_url=acs_url,
        sso_url=sso_url,
        idp_public_key=idp_public_key,
        sp_public_key=sp_public_key,
        encryption_key=encryption_key,
        default_exp=default_exp,
        allowed_clock_skew=allowed_clock_skew,
        want_assertions_signed=want_assertions_signed,
        replay_ttl=replay_ttl,
    )


__all__ = [
    "BaseSAML",
    "SAML",
    "SAMLSubject",
    "SAMLConditions",
    "SAMLAuthnStatement",
    "SAMLAssertion",
    "SAMLResponse",
    "SAMLRequest",
    "SAMLAttributeQuery",
    "SAMLArtifactResolve",
    "SAMLArtifactResponse",
    "SAMLLogoutRequest",
    "SAMLLogoutResponse",
    "SAMLManageNameIDRequest",
    "SAMLManageNameIDResponse",
    "SAMLMetadata",
    "create_instance",
]
