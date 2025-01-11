# -*- coding: utf-8 -*-


from pydantic import BaseModel


class Tokens(BaseModel):
    access: str
    refresh: str
