# -*- coding: utf-8 -*-

from typing import Union

from cryptography.hazmat.primitives.asymmetric import ec, rsa


KeyLike = Union[
    str,
    bytes,
    rsa.RSAPrivateKey,
    rsa.RSAPublicKey,
    ec.EllipticCurvePrivateKey,
    ec.EllipticCurvePublicKey,
]
