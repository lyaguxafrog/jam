# -*- coding: utf-8 -*-

from .base import JamConfigurationError, JamError, JamValidationError


class JamSAMLError(JamError):
    default_message = "SAML error occurred."
    default_code = "saml.error"


class JamSAMLExpired(JamError):
    default_message = "SAML assertion has expired."
    default_code = "saml.assertion_expired"


class JamSAMLNotYetValid(JamError):
    default_message = "SAML assertion is not yet valid."
    default_code = "saml.assertion_not_yet_valid"


class JamSAMLInvalidAudience(JamError):
    default_message = "SAML assertion audience validation failed."
    default_code = "saml.invalid_audience"


class JamSAMLInvalidIssuer(JamError):
    default_message = "SAML assertion issuer validation failed."
    default_code = "saml.invalid_issuer"


class JamSAMLEmptyPrivateKey(JamConfigurationError):
    default_message = "For SAML signing, you must specify `private_key`."
    default_code = "saml.config.empty_private_key"


class JamSAMLEmptyPublicKey(JamConfigurationError):
    default_message = "For SAML verification, you must specify `public_key`."
    default_code = "saml.config.empty_public_key"


class JamSAMLUnsupportedAlgorithm(JamConfigurationError):
    default_message = "Unsupported SAML algorithm."
    default_code = "saml.config.unsupported_algorithm"


class JamSAMLValidationError(JamValidationError):
    default_message = "SAML assertion validation failed."
    default_code = "saml.validation.assertion_error"
