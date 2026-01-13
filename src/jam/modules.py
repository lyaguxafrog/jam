# -*- coding: utf-8 -*-

"""This module is deprecated.

All modules now use factory functions (create_instance) instead of wrapper classes.

For backward compatibility, BaseModule is kept for aio.modules.
"""


class BaseModule:
    """The base module from which all other modules inherit."""

    def __init__(
        self,
        module_type: str = "custom",
    ) -> None:
        """Class constructor.

        Args:
            module_type (str): Type of module
        """
        self._type = module_type


# SessionModule and OAuth2Module have been removed.
# Use create_instance functions from respective modules:
#   - jam.sessions.create_instance
#   - jam.oauth2.create_instance
