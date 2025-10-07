# -*- coding: utf-8 -*-

"""Async OAuth2 modules."""

from .builtin.github import GitHubOAuth2Client
from .builtin.gitlab import GitLabOAuth2Client
from .builtin.google import GoogleOAuth2Client
from .builtin.yandex import YandexOAuth2Client


__all__ = [
    "GitLabOAuth2Client",
    "GitHubOAuth2Client",
    "GoogleOAuth2Client",
    "YandexOAuth2Client",
]
