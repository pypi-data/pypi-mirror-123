#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Common constant variables for test cases."""
import itertools
import pathlib
import typing


def get_basename(path: str) -> str:
    """Extract basename from given path ``path``."""
    return pathlib.Path(path).name.replace('.py', '').replace('test_', '')


def concat(xss: typing.Iterable[typing.Iterable[typing.Any]]
           ) -> typing.Iterator[typing.Any]:
    """Concat an iterable of iterables."""
    return itertools.chain.from_iterable(xs for xs in xss)

# vim:sw=4:ts=4:et:
