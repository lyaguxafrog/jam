# -*- coding: utf-8 -*-

"""All Jam exceptions
"""

from .base import JamConfigurationError, JamError, JamValidationError
from .jose import JamJWSVerificationError
from .jwt import (
    JamJWTEmptyPrivateKey,
    JamJWTEmptySecretKey,
    JamJWTExpired,
    JamJWTInBlackList,
    JamJWTNotInWhiteList,
    JamJWTUnsupportedAlgorithm,
    JamJWTValidationError,
)
from .oauth2 import (
    JamOAuth2EmptyRaw,
    JamOAuth2Error,
    JamOAuth2ProviderNotConfigured,
)
from .paseto import (
    JamPASETOInvalidED25519Key,
    JamPASETOInvalidPurpose,
    JamPASETOInvalidRSAKey,
    JamPASETOInvalidSecp384r1Key,
    JamPASETOInvalidSymmetricKey,
    JamPASETOInvalidTokenFormat,
    JamPASTOKeyVerificationError,
)
from .plugins import (
    JamFlaskPluginConfigError,
    JamFlaskPluginError,
    JamLitestarPluginConfigError,
    JamLitestarPluginError,
    JamStarlettePluginConfigError,
    JamStarlettePluginError,
)
from .sessions import (
    JamSessionEmptyAESKey,
    JamSessionNotFound,
)


__all__ = [
    "JamError",
    "JamConfigurationError",
    "JamValidationError",
    "JamOAuth2Error",
    "JamOAuth2EmptyRaw",
    "JamOAuth2ProviderNotConfigured",
    "JamJWTExpired",
    "JamJWTInBlackList",
    "JamJWTNotInWhiteList",
    "JamJWTEmptyPrivateKey",
    "JamJWTEmptySecretKey",
    "JamJWTUnsupportedAlgorithm",
    "JamJWTValidationError",
    "JamJWSVerificationError",
    "JamPASETOInvalidSymmetricKey",
    "JamPASETOInvalidRSAKey",
    "JamPASETOInvalidED25519Key",
    "JamPASETOInvalidSecp384r1Key",
    "JamPASETOInvalidPurpose",
    "JamPASETOInvalidTokenFormat",
    "JamPASTOKeyVerificationError",
    "JamLitestarPluginConfigError",
    "JamLitestarPluginError",
    "JamFlaskPluginConfigError",
    "JamFlaskPluginError",
    "JamStarlettePluginConfigError",
    "JamStarlettePluginError",
    "JamSessionNotFound",
    "JamSessionEmptyAESKey",
]
