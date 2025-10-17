# -*- coding: utf-8 -*-

"""
JAM - Universal auth* library

Source code: https://github.com/lyaguxafrog/jam
Documentation: https://jam.makridenko.ru
"""

from jam.__abc_encoder__ import BaseEncoder
from jam.__abc_instances__ import BaseJam
from jam.encoders import JsonEncoder
from jam.instance import Jam


__version__ = "2.6.0a5"
__all__ = ["Jam", "JsonEncoder", "BaseJam", "BaseEncoder"]
