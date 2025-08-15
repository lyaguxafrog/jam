# -*- coding: utf-8 -*-

"""Logger configuration for package."""

import logging

_LOG_FORMAT = "%(name)s | %(levelname)s - %(message)s"

logging.basicConfig(format=_LOG_FORMAT)
logger = logging.getLogger("jam")

