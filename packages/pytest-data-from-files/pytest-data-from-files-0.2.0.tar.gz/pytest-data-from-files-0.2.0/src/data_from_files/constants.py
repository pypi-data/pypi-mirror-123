#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Constant variables."""
import re
import typing


OPT_TEST_ROOT: str = '--test-root'
OPT_DATADIR_NAME: str = '--test-data-dirname'
OPT_DATA_PATTERN: str = '--test-data-pattern'

TEST_ROOT: str = 'tests'
DATADIR_NAME: str = 'data'
DATA_PATTERN: str = '**/*.*'

NAME_PATTERN: typing.Pattern = re.compile(
    r'^test_([^.]+)\.py.*$',
    re.IGNORECASE
)

PY_DATA_VAR_NAME: str = 'DATA'

TEXT_FILE_EXTS: typing.Tuple[str, ...] = (
    '.txt', '.md', '.rst'
)

# vim:sw=4:ts=4:et:
