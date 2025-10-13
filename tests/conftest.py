# -*- coding: utf-8 -*-

import asyncio

from fakeredis import FakeStrictRedis
from pytest import fixture

from jam.tests import TestAsyncJam


# @fixture(scope="function")
# def fake_redis():
#     return FakeStrictRedis()


def _async_mock(self, return_value=None):
    async def _mock(*args, **kwargs):
        await asyncio.sleep(0)
        return return_value

    return _mock


def _mock(self, return_value=None):
    return return_value


TestAsyncJam._async_mock = _async_mock
