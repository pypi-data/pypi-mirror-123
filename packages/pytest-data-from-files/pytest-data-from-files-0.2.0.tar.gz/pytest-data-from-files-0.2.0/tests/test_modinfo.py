#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for .modinfo."""
import pathlib

import pytest

import data_from_files.modinfo as TT

from . import constants


def test_get_target_module_path(request):
    res = TT.get_target_module_path(request)
    assert res == pathlib.Path(__file__)


@pytest.mark.parametrize(
    ('args', 'exp'),
    (
     ((pathlib.Path('a/b.json'), 'a'), [pathlib.Path('a')]),
     ((pathlib.Path('/a/b.json'), 'a'), [pathlib.Path('/a')]),
     ((pathlib.Path('/a/b/c/e/f/g/h.py'), 'c'),
      [pathlib.Path('/a/b/c/e/f/g'), pathlib.Path('/a/b/c/e/f'),
       pathlib.Path('/a/b/c/e'), pathlib.Path('/a/b/c')
       ]),
     )
)
def test_find_parent_dirs(args, exp):
    assert TT.find_parent_dirs(*args) == exp


@pytest.mark.parametrize(
    ('args', 'excs'),
    (
     ((pathlib.Path('__file__'), 'invalid_root'), (ValueError, )),
     )
)
def test_find_parent_dirs_failures(args, excs):
    with pytest.raises(excs):
        _ = TT.find_parent_dirs(*args)


def test_get_test_data_info_for_target(request):
    res = TT.get_test_data_info_for_target(request)
    assert res.root == constants.CURDIR
    assert res.datadir == constants.DATADIR / 'modinfo'

    subdirs = res.subdirs
    assert subdirs
    assert subdirs == ['10']  # tests/data/modinfo/*.

# vim:sw=4:ts=4:et:
