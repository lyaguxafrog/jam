# -*- coding: utf-8 -*-

from fakeredis import FakeStrictRedis
from pytest import fixture


@fixture(scope="function")
def fake_redis():
    return FakeStrictRedis()
