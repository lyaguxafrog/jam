# -*- coding: utf-8 -*-

from .base import JamError, JamValidationError, JamConfigurationError


class JamJWTExpired(JamError):
    default_message = "Token lifetime expired."
    default_code = "jwt.token_expired"


class JamJWTInBlackList(JamError):
    default_message = "Token in blacklist."
    default_code = "jwt.blacklist"


class JamJWTNotInWhiteList(JamError):
    default_message = "Token not in whitelist."
    default_code = "jwt.whitelist"


class JamJWTEmptySecretKey(JamConfigurationError):
    default_message = "For symmetric encryption, you must specify `secret_key`."
    default_code = "jwt.config.empty_secret_key"


class JamJWTEmptyPrivateKey(JamConfigurationError):
    default_message = "For asymmetric encryption, you must specify `private_key`."
    default_code = "jwt.config.empty_private_key"


class JamJWTUnsupportedAlgorithm(JamConfigurationError):
    default_message = "Unsupported JWT algorithm."
    default_code = "jwt.config.unsupported_algorithm"


class JamJWTValidationError(JamValidationError):
    default_message = "Token validation failed."
    default_code = "jwt.validation.token_validation_error"
