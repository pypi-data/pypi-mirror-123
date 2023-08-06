#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for .load."""
import pathlib

import pytest

import data_from_files.loader as TT

from . import constants

if TT.any_load:
    import anyconfig


EXCS = (FileNotFoundError, ValueError, RuntimeError)
if TT.any_load is not None:
    EXCS = (
        anyconfig.UnknownFileTypeError,
        *EXCS
    )

PY_PATH_0 = constants.CURDIR / 'constants.py'


@pytest.mark.parametrize(
    ('args', 'exp'),
    (
     ((PY_PATH_0, ), constants.DATA),
     ((str(PY_PATH_0), ), constants.DATA),
     ((PY_PATH_0, 'DATA'), constants.DATA),
     )
)
def test_load_from_py(args, exp):
    assert TT.load_from_py(*args) == exp, f'args: {args!r}, exp: {exp!r}'


PY_DATA_PATH_0 = constants.DATADIR / '20/input/00.py'
PY_DATA_0 = TT.json.load(
    (constants.DATADIR / '20/expected/00.json').open()
)


@pytest.mark.parametrize(
    ('arg', 'exp'),
    ((PY_DATA_PATH_0, PY_DATA_0),
     )
)
def test_load_literal_data_from_py(arg, exp):
    assert TT.load_literal_data_from_py(arg) == exp


TXT_DATA_PATHS = (constants.DATADIR / '40/input').glob('*.txt')
TXT_DATA_PAIRS = [
    ((p, ),
     TT.json.load(
        (constants.DATADIR / f'40/expected/{p.name.replace(".txt", ".json")}'
         ).open()
     ))
    for p in TXT_DATA_PATHS
]
JSON_DATA_PATHS = (constants.DATADIR / '10/input').glob('*.json')
JSON_DATA_PAIRS = [
    ((p, ),
     TT.json.load(
        (constants.DATADIR / f'10/expected/{p.name.replace(".txt", ".json")}'
         ).open()
     ))
    for p in JSON_DATA_PATHS
]


@pytest.mark.parametrize(
    ('args', 'exp'),
    (
     *TXT_DATA_PAIRS,
     ((PY_DATA_PATH_0, ), PY_DATA_0),
     *JSON_DATA_PAIRS,
     )
)
def test_load_from_path(args, exp):
    assert TT.load_from_path(*args) == exp


@pytest.mark.parametrize(
    'arg',
    (pathlib.Path('file_does_not_exist.json'),
     constants.CURDIR / '..' / 'LICENSE.MIT',
     )
)
def test_load_from_path_failure(arg):
    with pytest.raises(EXCS):
        _ = TT.load_from_path(arg)


TXT_DIR_DATA = (
    constants.DATADIR / '40/input',
    [
        (TT.json.load(p.open()),
         pathlib.Path(
            str(p).replace('expected', 'input').replace('.json', '.txt')
         )
         ) for p in (constants.DATADIR / '40/expected').glob('*.json')
    ]
)
JSON_DIR_DATA = (
    constants.DATADIR / '10/input',
    [
        (TT.json.load(p.open()),
         pathlib.Path(str(p).replace('expected', 'input'))
         ) for p in (constants.DATADIR / '10/expected').glob('*.json')
    ]
)


@pytest.mark.parametrize(
    ('datadir', 'exp'),
    (
     TXT_DIR_DATA,
     JSON_DIR_DATA,
     )
)
def test_each_data_under_dir(datadir, exp):
    res = list(TT.each_data_under_dir(datadir, constants.DATA_PATTERN))
    assert len(res) == len(exp)
    for data, (exp_data, path) in zip(res, exp):
        assert data.data == exp_data
        assert data.path == path


def test_load_datasets_from_dir_failures(tmp_path):
    path = tmp_path / 'test.json'
    path.touch()

    with pytest.raises(EXCS):
        _ = list(
            TT.each_data_under_dir(path, constants.DATA_PATTERN, safe=False)
        )

# vim:sw=4:ts=4:et:
