# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, TypedDict


class SAMLAssertion(TypedDict):
    """SAML assertion data structure."""

    subject: str
    issuer: str
    audience: str
    attributes: dict[str, Any]
    issued_at: datetime
    expires_at: datetime


class SAMLConditions(TypedDict, total=False):
    """Optional SAML conditions."""

    not_before: datetime
    not_on_or_after: datetime
    audience_restriction: list[str]
