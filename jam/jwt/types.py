# -*- coding: utf-8 -*-

from typing import Literal, TypedDict, Union


class BaseListConfig(TypedDict):
    """Base config typedict."""

    list_type: Literal["redis", "json", "custom"]
    type: Literal["black", "white"]


class RedisListConfig(BaseListConfig):
    """Redis lists config."""

    redis_uri: str
    in_list_life_time: int


class JSONListConfig(BaseListConfig):
    """Json lists config."""

    json_path: str


class CustomListConfig(BaseListConfig, total=False):
    """Custom list config."""

    custom_module: str


ListConfig = Union[
    RedisListConfig, JSONListConfig, CustomListConfig, BaseListConfig
]
