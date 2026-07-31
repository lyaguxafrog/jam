# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from jam.saml.types import (
    SAMLArtifactResolve,
    SAMLArtifactResponse,
    SAMLAttributeQuery,
    SAMLLogoutRequest,
    SAMLLogoutResponse,
    SAMLManageNameIDRequest,
    SAMLManageNameIDResponse,
    SAMLRequest,
    SAMLResponse,
)


class BaseSAML(ABC):
    """SAML 2.0 module.

    Supports both Service Provider (SP) and Identity Provider (IdP) roles.
    """

    # ── SP: accepting logins from external IdPs ──

    @abstractmethod
    def prepare_authn_request(
        self,
        idp_sso_url: str,
        *,
        acs_url: str,
        binding: str = "redirect",
        **kwargs: Any,
    ) -> str:
        """Build an AuthnRequest for the given IdP SSO URL.

        Args:
            idp_sso_url: IdP single sign-on endpoint URL.
            acs_url: SP assertion consumer service URL.
            binding: ``"redirect"`` (default) or ``"post"``.
            **kwargs: Extra params (relay_state, force_authn, etc.).

        Returns:
            Redirect: IdP URL with signed AuthnRequest.
            POST: Base64-encoded SAMLRequest as a string (embed in form).
        """
        raise NotImplementedError

    @abstractmethod
    def parse_response(
        self,
        saml_response: str,
        *,
        binding: str = "post",
        **kwargs: Any,
    ) -> SAMLResponse:
        """Parse and validate a SAML Response from an IdP.

        Automatically decrypts ``<saml:EncryptedAssertion>`` if the
        instance has a ``private_key`` configured.

        Args:
            saml_response: Raw SAMLResponse data (Base64 string for POST,
                           query-string for Redirect).
            binding: ``"post"`` (default) or ``"redirect"``.
            **kwargs: Expected audience, expected issuer, etc.

        Returns:
            Parsed SAMLResponse with assertion data.

        Raises:
            JamSAMLExpired: Assertion is expired.
            JamSAMLNotYetValid: Assertion is not yet valid.
            JamSAMLInvalidAudience: Audience doesn't match.
            JamSAMLInvalidIssuer: Issuer doesn't match.
            JamSAMLValidationError: Signature verification failed.
        """
        raise NotImplementedError

    # ── IdP: issuing SAML assertions ──

    @abstractmethod
    def build_response(
        self,
        subject: str,
        attributes: dict[str, Any],
        *,
        issuer: str,
        audience: str,
        **kwargs: Any,
    ) -> str:
        """Build (and optionally encrypt) a SAML Response containing an Assertion.

        Args:
            subject: The authenticated user identifier.
            attributes: User attributes (email, roles, etc.).
            issuer: IdP entity ID.
            audience: SP entity ID (the intended audience).
            **kwargs: in_response_to, name_id_format, session_index,
                      encrypt (bool, default False).

        Returns:
            Signed (and optionally encrypted) SAML Response XML string.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_authn_request(
        self,
        saml_request: str,
        *,
        binding: str = "redirect",
        **kwargs: Any,
    ) -> SAMLRequest:
        """Parse an incoming AuthnRequest from an SP.

        Args:
            saml_request: Raw SAMLRequest data.
            binding: ``"redirect"`` (default) or ``"post"``.
            **kwargs: Expected issuer (for validation).

        Returns:
            Parsed SAMLRequest data.

        Raises:
            JamSAMLInvalidIssuer: Issuer doesn't match expected.
        """
        raise NotImplementedError

    # ── SLO: Single Logout ──

    @abstractmethod
    def build_logout_request(
        self,
        name_id: str,
        *,
        issuer: str,
        destination: str,
        session_index: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Build a SAML LogoutRequest.

        Args:
            name_id: The user identifier being logged out.
            issuer: Entity ID of the sender (IdP or SP).
            destination: SLO endpoint URL of the recipient.
            session_index: Session identifier (optional).
            **kwargs: Extra params (binding, relay_state, etc.).

        Returns:
            Signed LogoutRequest XML (POST → Base64, Redirect → URL).
        """
        raise NotImplementedError

    @abstractmethod
    def parse_logout_request(
        self,
        saml_request: str,
        *,
        binding: str = "redirect",
        **kwargs: Any,
    ) -> SAMLLogoutRequest:
        """Parse a SAML LogoutRequest.

        Args:
            saml_request: Raw LogoutRequest data.
            binding: ``"redirect"`` (default) or ``"post"``.
            **kwargs: issuer (expected issuer for validation).

        Returns:
            Parsed SAMLLogoutRequest.

        Raises:
            JamSAMLInvalidIssuer: Issuer doesn't match expected.
        """
        raise NotImplementedError

    @abstractmethod
    def build_logout_response(
        self,
        in_response_to: str,
        *,
        issuer: str,
        destination: str,
        status_code: str = "urn:oasis:names:tc:SAML:2.0:status:Success",
        **kwargs: Any,
    ) -> str:
        """Build a SAML LogoutResponse.

        Args:
            in_response_to: ID of the LogoutRequest being responded to.
            issuer: Entity ID of the sender.
            destination: SLO endpoint URL of the recipient.
            status_code: SAML status code (default Success).
            **kwargs: Extra params (binding, relay_state, etc.).

        Returns:
            Signed LogoutResponse XML (POST → Base64, Redirect → URL).
        """
        raise NotImplementedError

    @abstractmethod
    def parse_logout_response(
        self,
        saml_response: str,
        *,
        binding: str = "redirect",
        **kwargs: Any,
    ) -> SAMLLogoutResponse:
        """Parse a SAML LogoutResponse.

        Args:
            saml_response: Raw LogoutResponse data.
            binding: ``"redirect"`` (default) or ``"post"``.
            **kwargs: issuer (expected issuer for validation).

        Returns:
            Parsed SAMLLogoutResponse.

        Raises:
            JamSAMLInvalidIssuer: Issuer doesn't match expected.
        """
        raise NotImplementedError

    # ── Metadata ──

    @abstractmethod
    def generate_metadata(
        self,
        *,
        entity_id: str,
        sso_url: str | None = None,
        acs_url: str | None = None,
        role: str | None = None,
    ) -> str:
        """Generate SAML 2.0 metadata XML.

        Args:
            entity_id: Entity ID of the IdP or SP.
            sso_url: SSO URL (required for IdP metadata).
            acs_url: ACS URL (required for SP metadata).
            role: ``"idp"`` or ``"sp"``. Auto-detected if omitted.

        Returns:
            SAML metadata XML string.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_metadata(self, metadata_xml: str) -> Any:
        """Parse SAML 2.0 metadata XML.

        Args:
            metadata_xml: Raw metadata XML string.

        Returns:
            SAMLMetadata with parsed fields.
        """
        raise NotImplementedError

    # ── Attribute Query ──

    @abstractmethod
    def build_attribute_query(
        self,
        subject: str,
        *,
        issuer: str,
        destination: str,
        attribute_names: list[str] | None = None,
        binding: str = "post",
        **kwargs: Any,
    ) -> str:
        """Build a SAML AttributeQuery.

        Args:
            subject: The subject to query attributes for.
            issuer: Entity ID of the requester (SP).
            destination: IdP attribute query endpoint URL.
            attribute_names: Specific attributes to request (None = all).
            binding: ``"post"`` (default) or ``"redirect"``.
            **kwargs: relay_state, etc.

        Returns:
            POST: Base64-encoded signed XML.
            Redirect: Signed redirect URL.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_attribute_query(
        self,
        saml_request: str,
        *,
        binding: str = "redirect",
        **kwargs: Any,
    ) -> SAMLAttributeQuery:
        """Parse an incoming SAML AttributeQuery.

        Args:
            saml_request: Raw AttributeQuery data.
            binding: ``"redirect"`` (default) or ``"post"``.
            **kwargs: issuer (expected issuer for validation).

        Returns:
            Parsed SAMLAttributeQuery.
        """
        raise NotImplementedError

    @abstractmethod
    def build_attribute_query_response(
        self,
        in_response_to: str,
        subject: str,
        attributes: dict[str, Any],
        *,
        issuer: str,
        audience: str,
        **kwargs: Any,
    ) -> str:
        """Build a SAML Response for an AttributeQuery.

        Args:
            in_response_to: AttributeQuery ID being responded to.
            subject: The subject.
            attributes: User attributes dict.
            issuer: IdP entity ID.
            audience: SP entity ID.
            **kwargs: destination, name_id_format.

        Returns:
            Signed SAML Response XML string.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_attribute_query_response(
        self,
        saml_response: str,
        *,
        binding: str = "post",
        **kwargs: Any,
    ) -> SAMLResponse:
        """Parse a SAML Response from an AttributeQuery.

        Delegates to parse_response.

        Args:
            saml_response: Raw SAMLResponse data.
            binding: ``"post"`` (default) or ``"redirect"``.
            **kwargs: audience, issuer, etc.

        Returns:
            Parsed SAMLResponse.
        """
        raise NotImplementedError

    # ── Artifact Binding ──

    @abstractmethod
    def build_artifact(self, source_message_id: str, *, issuer: str) -> str:
        """Create a SAML 2.0 artifact (Base64 string).

        Args:
            source_message_id: The ID of the message the artifact references.
            issuer: Entity ID of the issuer.

        Returns:
            Base64-encoded artifact string.
        """
        raise NotImplementedError

    @abstractmethod
    def build_artifact_resolve(
        self,
        artifact: str,
        *,
        issuer: str,
        destination: str,
        **kwargs: Any,
    ) -> str:
        """Build a SAML ArtifactResolve.

        Args:
            artifact: The artifact to resolve.
            issuer: Entity ID of the requester (SP).
            destination: IdP artifact resolution service URL.
            **kwargs: binding ("post" or "redirect" or "soap").

        Returns:
            Signed ArtifactResolve XML / SOAP envelope.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_artifact_resolve(
        self,
        saml_request: str,
        *,
        binding: str = "post",
        **kwargs: Any,
    ) -> SAMLArtifactResolve:
        """Parse an incoming SAML ArtifactResolve.

        Args:
            saml_request: Raw ArtifactResolve data.
            binding: ``"post"`` (default), ``"redirect"``, or ``"soap"``.
            **kwargs: issuer (expected issuer for validation).

        Returns:
            Parsed SAMLArtifactResolve.
        """
        raise NotImplementedError

    @abstractmethod
    def build_artifact_response(
        self,
        in_response_to: str,
        original_message_xml: str,
        *,
        issuer: str,
        destination: str,
        **kwargs: Any,
    ) -> str:
        """Build a SAML ArtifactResponse wrapping the original message.

        Args:
            in_response_to: ArtifactResolve ID being responded to.
            original_message_xml: The original XML message to embed.
            issuer: Entity ID of the responder (IdP).
            destination: SP endpoint URL.
            **kwargs: binding, status_code.

        Returns:
            Signed ArtifactResponse XML / SOAP envelope.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_artifact_response(
        self,
        saml_response: str,
        *,
        binding: str = "post",
        **kwargs: Any,
    ) -> SAMLArtifactResponse:
        """Parse a SAML ArtifactResponse.

        Args:
            saml_response: Raw ArtifactResponse data.
            binding: ``"post"`` (default), ``"redirect"``, or ``"soap"``.
            **kwargs: issuer (expected issuer).

        Returns:
            Parsed SAMLArtifactResponse.
        """
        raise NotImplementedError

    @abstractmethod
    def resolve_artifact(
        self,
        artifact: str,
        *,
        issuer: str,
        resolve_url: str,
        **kwargs: Any,
    ) -> str:
        """Resolve a SAML artifact via SOAP to the IdP's resolve endpoint.

        Args:
            artifact: The artifact to resolve.
            issuer: Entity ID of the requester (SP).
            resolve_url: IdP artifact resolution service URL.
            **kwargs: Extra params (timeout, headers, expected_issuer, etc.).

        Returns:
            The original SAML message XML extracted from the ArtifactResponse.
        """
        raise NotImplementedError

    # ── NameID Management ──

    @abstractmethod
    def build_manage_name_id_request(
        self,
        name_id: str,
        *,
        issuer: str,
        destination: str,
        new_id: str | None = None,
        binding: str = "post",
        **kwargs: Any,
    ) -> str:
        """Build a SAML ManageNameIDRequest.

        Args:
            name_id: Current NameID.
            issuer: Entity ID of the requester.
            destination: Entity endpoint URL.
            new_id: New identifier (None = terminate).
            binding: ``"post"`` (default) or ``"redirect"``.
            **kwargs: relay_state, name_id_format.

        Returns:
            POST: Base64-encoded signed XML.
            Redirect: Signed redirect URL.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_manage_name_id_request(
        self,
        saml_request: str,
        *,
        binding: str = "redirect",
        **kwargs: Any,
    ) -> SAMLManageNameIDRequest:
        """Parse a SAML ManageNameIDRequest.

        Args:
            saml_request: Raw ManageNameIDRequest data.
            binding: ``"redirect"`` (default) or ``"post"``.
            **kwargs: issuer (expected issuer).

        Returns:
            Parsed SAMLManageNameIDRequest.
        """
        raise NotImplementedError

    @abstractmethod
    def build_manage_name_id_response(
        self,
        in_response_to: str,
        *,
        issuer: str,
        destination: str,
        status_code: str = "urn:oasis:names:tc:SAML:2.0:status:Success",
        **kwargs: Any,
    ) -> str:
        """Build a SAML ManageNameIDResponse.

        Args:
            in_response_to: ManageNameIDRequest ID.
            issuer: Entity ID of the responder.
            destination: Endpoint URL of the requester.
            status_code: SAML status code (default Success).
            **kwargs: binding, relay_state.

        Returns:
            POST: Base64-encoded signed XML.
            Redirect: Signed redirect URL.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_manage_name_id_response(
        self,
        saml_response: str,
        *,
        binding: str = "redirect",
        **kwargs: Any,
    ) -> SAMLManageNameIDResponse:
        """Parse a SAML ManageNameIDResponse.

        Args:
            saml_response: Raw ManageNameIDResponse data.
            binding: ``"redirect"`` (default) or ``"post"``.
            **kwargs: issuer (expected issuer).

        Returns:
            Parsed SAMLManageNameIDResponse.
        """
        raise NotImplementedError
