# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Token:
    """Data for Authresult."""

    token: str | None
