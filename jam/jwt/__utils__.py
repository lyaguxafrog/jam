# -*- coding: utf-8 -*-

import base64


def __base64url_encode__(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def __base64url_decode__(data):
    padding = "=" * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)
