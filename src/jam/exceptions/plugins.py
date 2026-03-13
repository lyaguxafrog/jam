# -*- coding: utf-8 -*-

from jam.exceptions.base import JamConfigurationError, JamError


class JamLitestarPluginConfigError(JamConfigurationError):
    """Exception raised when a configuration error occurs for a litestar plugin."""

    default_message = "Configuration error occurred for a litestar plugin."
    default_code = "jam.configuration.plugin.litestar"


class JamLitestarPluginError(JamError):
    """Exception raised when an error occurs for a litestar plugin."""

    default_message = "An error occurred for a litestar plugin."
    default_code = "jam.plugin.litestar"


class JamFlaskPluginConfigError(JamConfigurationError):
    """Exception raised when a configuration error occurs for a flask plugin."""

    default_message = "Configuration error occurred for a flask plugin."
    default_code = "jam.configuration.plugin.flask"


class JamFlaskPluginError(JamError):
    """Exception raised when an error occurs for a flask plugin."""

    default_message = "An error occurred for a flask plugin."
    default_code = "jam.plugin.flask"

class JamStarlettePluginConfigError(JamConfigurationError):
    """Exception raised when a configuration error occurs for a starlette plugin."""

    default_message = "Configuration error occurred for a starlette plugin."
    default_code = "jam.configuration.plugin.starlette"


class JamStarlettePluginError(JamError):
    """Exception raised when an error occurs for a starlette plugin."""

    default_message = "An error occurred for a starlette plugin."
    default_code = "jam.plugin.starlette"
