# -*- coding: utf-8 -*-

from .base import JamError, JamConfigurationError, JamValidationError


class JamSessionNotFound(JamError):
    default_message = "Session not found."
    default_code = "sessions.not_found"
