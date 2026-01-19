# -*- coding: utf-8 -*-

"""JAM - Universal auth* library

Source code: https://github.com/lyaguxafrog/jam
Documentation: https://jam.makridenko.ru
"""

from jam.__base__ import BaseJam
from jam.__base_encoder__ import BaseEncoder
from jam.encoders import JsonEncoder
from jam.instance import Jam


__version__ = "3.0.0b0"
__all__ = ["Jam", "JsonEncoder", "BaseJam", "BaseEncoder"]
