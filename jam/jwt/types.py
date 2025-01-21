# -*- coding: utf-8 -*-


from pydantic import BaseModel


class Tokens(BaseModel):
    """
    Scop for tokens

    * access: str
    * refresh: str
    """

    access: str
    refresh: str
