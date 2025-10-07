# -*- coding: utf-8 -*-

"""OAuth2 module."""

from .__abc_oauth2_repo__ import BaseOAuth2Client
from .builtin.github import GitHubOAuth2Client
from .builtin.gitlab import GitLabOAuth2Client
from .builtin.google import GoogleOAuth2Client


__all__ = ["BaseOAuth2Client", "GitHubOAuth2Client"]
