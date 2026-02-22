# -*- coding: utf-8 -*-

from .base import JamError



class JamOAuth2Error(JamError):
    default_message = "OAuth2 error occurred."
    default_code = "oauth2.runtime_error"


class JamOAuth2EmptyRaw(JamError):
    default_message = "Empty response from token endpoint"
    default_code = "oauth2.empty_response"
