#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Pytest hooks."""
import typing

from . import constants

if typing.TYPE_CHECKING:
    from _pytest.config.argparsing import Parser


def pytest_addoption(parser: 'Parser') -> None:
    """Add a command line option for this plugin.

    .. seealso:: https://bit.ly/3B79aRK
    """
    parser.addoption(
        constants.OPT_TEST_ROOT, default=constants.TEST_ROOT,
        help='Specify the name of dir to keep test code and data [%(default)s]'
    )
    parser.addoption(
        constants.OPT_DATADIR_NAME, default=constants.DATADIR_NAME,
        help='Specify the name of sub dir to keep test data [%(default)s]'
    )
    parser.addoption(
        constants.OPT_DATA_PATTERN, default=constants.DATA_PATTERN,
        help='Specify the path pattern of test data files [%(default)s]'
    )

# vim:sw=4:ts=4:et:
