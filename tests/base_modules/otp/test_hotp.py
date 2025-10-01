# -*- coding: utf-8 -*-

import base64

import pytest

from jam.otp import HOTP


SECRET = base64.b32encode(b"12345678901234567890").decode("utf-8")


@pytest.fixture
def hotp():
    return HOTP(secret=SECRET, digits=6, digest="sha1")


def test_at_generates_code(hotp):
    code = hotp.at(0)

    assert len(code) == 6
    assert code.isdigit()


def test_verify_correct_code(hotp):
    counter = 0
    code = hotp.at(counter)

    assert hotp.verify(code, counter) is True


def test_verify_incorrect_code(hotp):
    counter = 0
    wrong_code = "000000"

    assert hotp.verify(wrong_code, counter) is False


def test_verify_with_look_ahead(hotp):
    counter = 0
    next_code = hotp.at(counter + 1)

    assert hotp.verify(next_code, counter, look_ahead=1) is True
    assert hotp.verify(next_code, counter, look_ahead=0) is False


def test_multiple_counters(hotp):
    codes = [hotp.at(i) for i in range(5)]

    for i, code in enumerate(codes):
        assert hotp.verify(code, i) is True
