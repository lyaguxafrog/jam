# -*- coding: utf-8 -*-

from .base import JamError, JamConfigurationError, JamValidationError


class JamPASETOInvalidRSAKey(JamConfigurationError):
    default_message = "Invalid RSA key."
    default_code = "paseto.configuration.invalid_rsa_key"


class JamPASETOInvalidED25519Key(JamConfigurationError):
    default_message = "Invalid ED25519 key."
    default_code = "paseto.configuration.invalid_ed25519_key"


class JamPASETOInvalidPurpose(JamValidationError):
    default_message = "Invalid purpose."
    default_code = "paseto.configuration.invalid_purpose"


class JamPASETOInvalidTokenFormat(JamValidationError):
    default_message = "Invalid token format."
    default_code = "paseto.validation.invalid_token_format"


class JamPASTOKeyVerificationError(JamError):
    default_message = "Key verification failed."
    default_code = "paseto.key_verification_failed"
