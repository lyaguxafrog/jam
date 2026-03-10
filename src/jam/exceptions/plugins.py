# -*- coding: utf-8 -*-

from jam.exceptions.base import JamConfigurationError


class JamLitestarPluginConfigError(JamConfigurationError):
    """Exception raised when a configuration error occurs for a litestar plugin."""

    default_message = "Configuration error occurred for a litestar plugin."
    default_code = "jam.configuration.plugin"
