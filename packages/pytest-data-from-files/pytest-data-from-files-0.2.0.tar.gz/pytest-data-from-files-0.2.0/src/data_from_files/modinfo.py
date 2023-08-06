#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Functions to get some meta info of the test target modules."""
import inspect
import itertools
import pathlib
import typing

from . import constants, datatypes

if typing.TYPE_CHECKING:
    import pytest


def get_name_from_path(path: pathlib.Path,
                       pattern: typing.Pattern = constants.NAME_PATTERN
                       ) -> str:
    """Get 'name' from given ``path``."""
    try:
        match = pattern.match(path.name)
        if match:
            return match.groups()[0]
    except (AttributeError, IndexError):
        pass

    return ''


def get_target_module_path(request: 'pytest.FixtureRequest'
                           ) -> pathlib.Path:
    """Resovle the path of the target module."""
    return pathlib.Path(inspect.getfile(request.module))


def find_parent_dirs(path: pathlib.Path, root_name: str
                     ) -> typing.List[pathlib.Path]:
    """Find out a series of sub dirs from the root dir named ``root_name``.

    >>> path = pathlib.Path('/a/b/c/e/f/g/h.py')
    >>> find_parent_dirs(path, 'c')  # doctest: +NORMALIZE_WHITESPACE
    [pathlib.Path('/a/b/c/e/f/g'), pathlib.Path('/a/b/c/e/f'),
     pathlib.Path('/a/b/c/e'), pathlib.Path('/a/b/c')]
    """
    if root_name not in path.parts:
        raise ValueError(f'Path {path!s} does not contain {root_name}')

    subdirs = list(
        itertools.takewhile(lambda x: x.name != root_name, path.parents)
    )

    if not subdirs:
        return [path.parent]

    return subdirs + [subdirs[-1].parent]


def get_test_data_info_for_target(request: 'pytest.FixtureRequest'
                                  ) -> datatypes.ModuleInfo:
    """Get some path info of the target module."""
    root_name = request.config.getoption(constants.OPT_TEST_ROOT)
    datadir_name = request.config.getoption(constants.OPT_DATADIR_NAME)

    path = get_target_module_path(request)
    name = get_name_from_path(path)

    parents = find_parent_dirs(path, root_name)
    root = parents[-1]

    if len(parents) == 1:  # no sub dirs.
        datadir = root / datadir_name / name
    else:
        datadir = root / datadir_name / parents[0].relative_to(root)

    return datatypes.ModuleInfo(
        root=root,
        datadir=datadir,
        subdirs=[d.name for d in datadir.glob('*') if d.is_dir()]
    )

# vim:sw=4:ts=4:et:
