# -*- coding: utf-8 -*-

from typing import Any

import flask

from jam.exceptions import JamFlaskPluginConfigError, JamFlaskPluginError
from jam.ext.flask.objects import BaseUser, Token
from jam.jwt import JWT
from jam.oauth2 import create_instance as create_oauth2
from jam.paseto import create_instance as create_paseto
from jam.sessions import create_instance as create_session
from jam.utils.config_maker import GENERIC_POINTER, __config_maker__


class BaseExtension:
    """Base Jam extension for Flask."""

    MODULE: Any
    _CONFIG_KEY: str

    def __init__(
        self,
        app: flask.Flask | None = None,
        auth: Any | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the extension.

        Args:
            app (flask.Flask | None): Flask application instance
            auth (Any | None): Pre-created auth module instance
            **kwargs: Configuration arguments
        """
        self.app = app
        self._auth = auth
        self._config = kwargs
        if app is not None:
            self.init_app(app)

    def init_app(self, app: flask.Flask) -> None:
        """Initialize the Flask application.

        Args:
            app (flask.Flask): Flask application instance
        """
        self.app = app
        if self._auth is None:
            self._auth = self.MODULE(**self._config)
        app.extensions[self._CONFIG_KEY] = self._auth


class BaseAuthExtension(BaseExtension):
    """Base Jam authentication extension for Flask."""

    MODULE: Any
    _CONFIG_KEY: str

    def __init__(
        self,
        app: flask.Flask | None = None,
        auth: Any | None = None,
        config: dict[str, Any] | str | None = None,
        pointer: str = GENERIC_POINTER,
        cookie_name: str | None = None,
        header_name: str | None = None,
        user: type[BaseUser] | None = None,
        bearer: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize the authentication extension.

        Args:
            app (flask.Flask | None): Flask application instance
            auth (Any | None): Pre-created auth module instance
            config (dict[str, Any] | str | None): Jam config as path/to/file or dict.
            pointer (str): Config pointer
            cookie_name (str | None): Cookie name to read token
            header_name (str | None): Header name to read token
            user (type[BaseUser]): User class for request
            bearer (bool): Strip "Bearer " prefix from header
            **kwargs: Configuration arguments if config=None
        """
        self._cookie_name = cookie_name
        self._header_name = header_name
        self._user = user
        self._bearer = bearer

        if not cookie_name and not header_name:
            raise JamFlaskPluginConfigError(
                message="Cookie name and header name cannot be both None.",
                details={
                    "cookie_name": cookie_name,
                    "header_name": header_name,
                },
            )

        if not user:
            raise JamFlaskPluginConfigError(
                message="User class cannot be None.",
                details={
                    "user": user,
                },
            )

        _config: dict[str, Any] | None = (
            __config_maker__(config, pointer) if config else None
        )

        params = _config.pop(self._CONFIG_KEY) if _config else kwargs

        super().__init__(app, auth=auth, **params)

    def _get_auth_token(self, request: flask.Request) -> str | None:
        token = None
        if self._header_name:
            token = request.headers.get(self._header_name, None)
            if token and self._bearer and token.startswith("Bearer "):
                token = token[7:]
        elif self._cookie_name:
            token = request.cookies.get(self._cookie_name, None)
        return token

    def load_user(
        self, request: flask.Request
    ) -> tuple[BaseUser | None, Token]:
        """Load user from request.

        Args:
            request (flask.Request): Flask request object

        Returns:
            tuple[BaseUser | None, Token]: User and token
        """
        raise NotImplementedError


class JWTExtension(BaseAuthExtension):
    """JWT extension for Flask."""

    MODULE = staticmethod(JWT)  # type: ignore
    _CONFIG_KEY = "jwt"

    def load_user(
        self, request: flask.Request
    ) -> tuple[BaseUser | None, Token]:
        """Load user from JWT token.

        Args:
            request (flask.Request): Flask request object

        Returns:
            tuple[BaseUser | None, Token]: User and token
        """
        token = self._get_auth_token(request)
        token_model = Token(token=token)
        if not token:
            return None, token_model
        try:
            data = self._auth.decode(token)
            user = self._user.from_payload(data)
            return user, token_model
        except Exception as e:
            raise JamFlaskPluginError(message=str(e))


class SessionExtension(BaseAuthExtension):
    """Session extension for Flask."""

    MODULE = staticmethod(create_session)
    _CONFIG_KEY = "sessions"

    def load_user(
        self, request: flask.Request
    ) -> tuple[BaseUser | None, Token]:
        """Load user from session.

        Args:
            request (flask.Request): Flask request object

        Returns:
            tuple[BaseUser | None, Token]: User and token
        """
        token = self._get_auth_token(request)
        token_model = Token(token=token)
        if not token:
            return None, token_model
        try:
            data = self._auth.get(token)
            if not data:
                return None, token_model
            user = self._user.from_payload(data)
            return user, token_model
        except Exception as e:
            raise JamFlaskPluginError(message=str(e))


class PASETOExtension(BaseAuthExtension):
    """PASETO extension for Flask."""

    MODULE = staticmethod(create_paseto)
    _CONFIG_KEY = "paseto"

    def load_user(
        self, request: flask.Request
    ) -> tuple[BaseUser | None, Token]:
        """Load user from PASETO token.

        Args:
            request (flask.Request): Flask request object

        Returns:
            tuple[BaseUser | None, Token]: User and token
        """
        token = self._get_auth_token(request)
        token_model = Token(token=token)
        if not token:
            return None, token_model
        try:
            data = self._auth.decode(token)
            if not data:
                return None, token_model
            payload = data[0] if isinstance(data, tuple) else data
            user = self._user.from_payload(payload)
            return user, token_model
        except Exception as e:
            raise JamFlaskPluginError(message=str(e))


class OAuth2Extension(BaseExtension):
    """OAuth2 extension for Flask."""

    MODULE = staticmethod(create_oauth2)
    _CONFIG_KEY = "oauth2"

    def __init__(
        self,
        app: flask.Flask | None = None,
        auth: Any | None = None,
        config: dict[str, Any] | str | None = None,
        pointer: str = GENERIC_POINTER,
        **kwargs: Any,
    ) -> None:
        """Initialize the OAuth2 extension.

        Args:
            app (flask.Flask | None): Flask application instance
            auth (Any | None): Pre-created auth module instance
            config (dict[str, Any] | str | None): Jam config as path/to/file or dict.
            pointer (str): Config pointer
            **kwargs: Configuration arguments if config=None
        """
        _config: dict[str, Any] | None = (
            __config_maker__(config, pointer) if config else None
        )

        params = _config.pop(self._CONFIG_KEY) if _config else kwargs
        super().__init__(app, auth=auth, **params)
