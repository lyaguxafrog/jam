# -*- coding: utf-8 -*-

"""
All Jam exceptions
"""

from .base import (
    JamError,
    JamConfigurationError,
    JamValidationError
)

from .oauth2 import (
    JamOAuth2Error,
    JamOAuth2EmptyRaw
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
    JamPASETOInvalidSymmetricKey,
    JamPASETOInvalidRSAKey,
    JamPASETOInvalidED25519Key,
    JamPASETOInvalidSecp384r1Key,
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
    "JamOAuth2Error",
    "JamOAuth2EmptyRaw",
    "JamJWTExpired",
    "JamJWTInBlackList",
    "JamJWTNotInWhiteList",
    "JamJWTEmptyPrivateKey",
    "JamJWTEmptySecretKey",
    "JamJWTUnsupportedAlgorithm",
    "JamJWTValidationError",
    "JamPASETOInvalidSymmetricKey",
    "JamPASETOInvalidRSAKey",
    "JamPASETOInvalidED25519Key",
    "JamPASETOInvalidSecp384r1Key",
    "JamPASETOInvalidPurpose",
    "JamPASETOInvalidTokenFormat",
    "JamPASTOKeyVerificationError",
    "JamSessionNotFound",
    "JamSessionEmptyAESKey",
]
