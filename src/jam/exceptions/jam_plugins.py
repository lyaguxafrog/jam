# -*- coding: utf-8 -*-

from jam.exceptions.base import JamError, JamConfigurationError


class JamPluginConfigurationError(JamConfigurationError):
    """Exception raised when a plugin configuration error occurs."""

    default_message = "Plugin configuration error occurred."
    default_code = "jam.plugin.configuration"
