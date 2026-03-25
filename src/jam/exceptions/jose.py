# -*- coding: utf-8 -*-

from .base import JamValidationError


class JamJWSVerificationError(JamValidationError):
    default_message = "JWS signature verification failed."
    default_code = "jws.verification_error"
