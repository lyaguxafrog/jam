# -*- coding: utf-8 -*-

"""
Module for making server auth sessions.

See docs: https://jam.makridenko.ru/
"""

from .__abc_session_repo__ import BaseSessionModule
from .json import JSONSessions
from .redis import RedisSessions
