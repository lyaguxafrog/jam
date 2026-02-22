# -*- coding: utf-8 -*-

"""
All Jam exceptions
"""

from .base import (
    JamError,
    JamConfigurationError,
    JamValidationError
)

from .jwt import (
    JamJWTExpired,
    JamJWTInBlackList,
    JamJWTNotInWhiteList,
    JamJWTEmptyPrivateKey,
    JamJWTEmptySecretKey,
    JamJWTUnsupportedAlgorithm,
    JamJWTValidationError,
)

from .paseto import (
    JamPASETOInvalidRSAKey,
    JamPASETOInvalidED25519Key,
    JamPASTOKeyVerificationError,
    JamPASETOInvalidPurpose,
    JamPASETOInvalidTokenFormat
)

from .sessions import (
    JamSessionNotFound,
    JamSessionEmptyAESKey,
)


__all__ = [
    "JamError",
    "JamConfigurationError",
    "JamValidationError",
    "JamJWTExpired",
    "JamJWTInBlackList",
    "JamJWTNotInWhiteList",
    "JamJWTEmptyPrivateKey",
    "JamJWTEmptySecretKey",
    "JamJWTUnsupportedAlgorithm",
    "JamJWTValidationError",
    "JamPASETOInvalidRSAKey",
    "JamPASETOInvalidED25519Key",
    "JamPASETOInvalidPurpose",
    "JamPASETOInvalidTokenFormat",
    "JamPASTOKeyVerificationError",
    "JamSessionNotFound",
    "JamSessionEmptyAESKey",
]
