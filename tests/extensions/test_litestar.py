# -*- coding: utf-8 -*-

import sys
from unittest.mock import Mock

import pytest
from litestar.config.app import AppConfig
from pytest_asyncio import fixture

from jam.ext.litestar.plugins import JamPlugin, JWTPlugin, SessionsPlugin
from jam.tests import TestAsyncJam, TestJam


@pytest.fixture
def jam() -> TestJam:
    return TestJam()


@fixture
async def async_jam() -> TestAsyncJam:
    return TestAsyncJam()


def test_jam_plugin_adds_dependency(jam):
    plugin = JamPlugin(jam=jam)
    app_config = AppConfig()

    updated_config = plugin.on_app_init(app_config)

    assert "jam" in updated_config.dependencies
    provider = updated_config.dependencies["jam"]
    assert callable(provider.dependency)
    assert provider.dependency() == jam


def test_jwt_plugin_adds_middleware_and_state(monkeypatch, jam):
    fake_middleware = Mock()

    monkeypatch.setitem(
        sys.modules,
        "jam.ext.litestar.middlewares",
        Mock(JamJWTMiddleware=fake_middleware),
    )

    app_config = AppConfig()
    plugin = JWTPlugin(jam=jam)

    updated_config = plugin.on_app_init(app_config)

    assert fake_middleware in updated_config.middleware  # middleware добавлен
    assert hasattr(updated_config.state, "jwt_middleware_settings")
    assert hasattr(updated_config.state, "jam_instance")
    assert updated_config.state.jam_instance == jam


def test_sessions_plugin_adds_middleware_and_state(monkeypatch, jam):
    fake_middleware = Mock()

    monkeypatch.setitem(
        sys.modules,
        "jam.ext.litestar.middlewares",
        Mock(JamSessionsMiddleware=fake_middleware),
    )

    app_config = AppConfig()
    plugin = SessionsPlugin(jam=jam)

    updated_config = plugin.on_app_init(app_config)

    assert fake_middleware in updated_config.middleware
    assert hasattr(updated_config.state, "session_middleware_settings")
    assert hasattr(updated_config.state, "session_instance")
    assert updated_config.state.session_instance == jam


@pytest.mark.asyncio
async def test_async_jam_plugin_adds_dependency(async_jam):
    plugin = JamPlugin(jam=async_jam)
    app_config = AppConfig()

    updated_config = plugin.on_app_init(app_config)

    assert "jam" in updated_config.dependencies
    provider = updated_config.dependencies["jam"]
    assert callable(provider.dependency)
    assert provider.dependency() == async_jam


@pytest.mark.asyncio
async def test_async_jwt_plugin_adds_middleware_and_state(
    monkeypatch, async_jam
):
    fake_middleware = Mock()

    monkeypatch.setitem(
        sys.modules,
        "jam.ext.litestar.middlewares",
        Mock(JamJWTMiddleware=fake_middleware),
    )

    app_config = AppConfig()
    plugin = JWTPlugin(jam=async_jam)

    updated_config = plugin.on_app_init(app_config)

    assert fake_middleware in updated_config.middleware  # middleware добавлен
    assert hasattr(updated_config.state, "jwt_middleware_settings")
    assert hasattr(updated_config.state, "jam_instance")
    assert updated_config.state.jam_instance == async_jam


@pytest.mark.asyncio
async def test_async_sessions_plugin_adds_middleware_and_state(
    monkeypatch, async_jam
):
    fake_middleware = Mock()

    monkeypatch.setitem(
        sys.modules,
        "jam.ext.litestar.middlewares",
        Mock(JamSessionsMiddleware=fake_middleware),
    )

    app_config = AppConfig()
    plugin = SessionsPlugin(jam=async_jam)

    updated_config = plugin.on_app_init(app_config)

    assert fake_middleware in updated_config.middleware
    assert hasattr(updated_config.state, "session_middleware_settings")
    assert hasattr(updated_config.state, "session_instance")
    assert updated_config.state.session_instance == async_jam
