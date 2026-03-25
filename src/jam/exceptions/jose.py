# -*- coding: utf-8 -*-

from .base import JamValidationError


class JamJWSVerificationError(JamValidationError):
    default_message = "JWS signature verification failed."
    default_code = "jws.verification_error"


class JamJWKValidationError(JamValidationError):
    default_message = "JWK validation failed."
    default_code = "jwk.validation_error"


class JamJWEEncryptionError(JamValidationError):
    default_message = "JWE encryption failed."
    default_code = "jwe.encryption_error"


class JamJWEDecryptionError(JamValidationError):
    default_message = "JWE decryption failed."
    default_code = "jwe.decryption_error"
