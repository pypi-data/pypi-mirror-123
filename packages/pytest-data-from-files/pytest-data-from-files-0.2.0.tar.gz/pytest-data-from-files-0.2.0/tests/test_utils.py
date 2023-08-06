#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for tests.utils."""
import pytest

from . import utils as TT


def test_get_basename():
    assert TT.get_basename(__file__) == 'utils'


@pytest.mark.parametrize(
    ('xss', 'exp'),
    (
     ([[]], []),
     ((()), []),
     ([[1, 2, 3], [4, 5]], [1, 2, 3, 4, 5]),
     ([[1, 2, 3], [4, 5, [6, 7]]], [1, 2, 3, 4, 5, [6, 7]]),
     (((1, 2, 3), (4, 5, (6, 7))), [1, 2, 3, 4, 5, (6, 7)]),
     (((i, i * 2) for i in range(3)), [0, 0, 1, 2, 2, 4]),
     )
)
def test_concat(xss, exp):
    assert list(TT.concat(xss)) == exp

# vim:sw=4:ts=4:et:
