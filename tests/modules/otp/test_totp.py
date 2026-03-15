# -*- coding: utf-8 -*-

import base64
import time

import pytest

from jam.otp import TOTP


@pytest.fixture
def totp():
    secret = base64.b32encode(b"12345678901234567890").decode("utf-8")
    return TOTP(secret=secret, digits=6, digest="sha1", interval=30)


def test_at_generates_code_fixed_time(totp):
    fixed_time = 1000000000
    code = totp.at(fixed_time)

    assert len(code) == 6
    assert code.isdigit()


def test_now_returns_current_code(totp):
    code = totp.now

    assert len(code) == 6
    assert code.isdigit()


def test_verify_correct_code_fixed_time(totp):
    fixed_time = 1000000000
    code = totp.at(fixed_time)

    assert totp.verify(code, fixed_time) is True


def test_verify_incorrect_code(totp):
    fixed_time = 1000000000
    wrong_code = "000000"

    assert totp.verify(wrong_code, fixed_time) is False


def test_verify_with_look_ahead(totp):
    fixed_time = 1000000000
    next_code = totp.at(fixed_time + 30)

    assert totp.verify(next_code, fixed_time, look_ahead=1) is True
    assert totp.verify(next_code, fixed_time, look_ahead=0) is False


def test_multiple_intervals(totp):
    base_time = 1000000000
    codes = [totp.at(base_time + i * 30) for i in range(5)]
    for i, code in enumerate(codes):
        assert totp.verify(code, base_time + i * 30) is True
