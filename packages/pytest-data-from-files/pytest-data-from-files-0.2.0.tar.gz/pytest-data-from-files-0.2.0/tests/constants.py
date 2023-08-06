#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Common constant variables for test cases."""
import pathlib


CURDIR = pathlib.Path(__file__).parent
DATADIR: pathlib.Path = CURDIR / 'data'

# .. seealso:: `~data_from_files.constants.DATA_PATTERN`
DATA_PATTERN: str = '**/*.*'

# Hardcode
PLUGIN_NAME = 'data_from_files'

# Example data for test cases.
DATA: str = '3.1415'

# vim:sw=4:ts=4:et:
