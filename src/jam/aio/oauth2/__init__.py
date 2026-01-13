# -*- coding: utf-8 -*-

"""Async OAuth2 modules."""

from typing import Any

from .builtin.github import GitHubOAuth2Client
from .builtin.gitlab import GitLabOAuth2Client
from .builtin.google import GoogleOAuth2Client
from .builtin.yandex import YandexOAuth2Client
from jam.oauth2.__abc_oauth2_repo__ import BaseOAuth2Client
from jam.logger import BaseLogger, logger


BUILTIN_PROVIDERS = {
    "github": "jam.aio.oauth2.builtin.github.GitHubOAuth2Client",
    "gitlab": "jam.aio.oauth2.builtin.gitlab.GitLabOAuth2Client",
    "google": "jam.aio.oauth2.builtin.google.GoogleOAuth2Client",
    "yandex": "jam.aio.oauth2.builtin.yandex.YandexOAuth2Client",
}


def create_instance(
    providers: dict[str, dict],
    logger: BaseLogger = logger,
    **kwargs: Any
) -> dict[str, BaseOAuth2Client]:
    """Create async OAuth2 clients for configured providers.

    Args:
        providers: {provider_name: {client_id, client_secret, redirect_uri, ...}}
        logger: Logger instance
        **kwargs: Additional params

    Returns:
        dict: {provider_name: OAuth2Client instance}
    """
    from jam.utils.config_maker import __module_loader__

    result = {}
    for name, cfg in providers.items():
        cfg = cfg.copy()  # Don't modify original config
        
        if "custom_module" in cfg:
            module_cls = __module_loader__(cfg.pop("custom_module"))
        else:
            module_path = BUILTIN_PROVIDERS.get(name, "jam.aio.oauth2.client.OAuth2Client")
            module_cls = __module_loader__(module_path)
        
        result[name] = module_cls(**cfg)
    
    return result


__all__ = [
    "GitLabOAuth2Client",
    "GitHubOAuth2Client",
    "GoogleOAuth2Client",
    "YandexOAuth2Client",
    "create_instance",
]
