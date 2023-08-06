#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# todo:
# type: ignore
"""Functions to load test data."""
import ast
import collections
import importlib.abc
import importlib.util
import json
import pathlib
import typing
import warnings

try:
    from anyconfig import load as any_load
except ImportError:
    any_load = None  # pylint: disable=invalid-name

try:
    from yaml import safe_load as yaml_load
except ImportError:
    yaml_load = None  # pylint: disable=invalid-name

from . import constants, datatypes


def load_from_py(path: pathlib.Path,
                 data_name: str = constants.PY_DATA_VAR_NAME
                 ) -> datatypes.DataT:
    """Load test data from .py files by evaluating it.

    .. note:: It's not safe.
    """
    spec = importlib.util.spec_from_file_location('testmod', str(path))
    if spec and isinstance(spec.loader, importlib.abc.Loader):
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        try:
            return getattr(mod, data_name, None)
        except (TypeError, ValueError, AttributeError):
            warnings.warn(f'No valid data "{data_name}" was found in {mod!r}.')

    return None


def load_literal_data_from_py(path: pathlib.Path) -> datatypes.DataT:
    """Load test data expressed by literal data from .py files.

    .. note:: It should be safer than the above function.
    """
    return ast.literal_eval(path.read_text().strip())


def load_from_path(path: pathlib.Path,
                   exec_py: bool = False,
                   keep_order: bool = False,
                   ) -> datatypes.DataT:
    """Load test data from given path ``path``.

    Test data files maybe loaded with anyconfig.load if it's available.
    """
    if path.suffix in constants.TEXT_FILE_EXTS:
        return path.read_text()

    if path.suffix == '.py':
        return (
            load_from_py if exec_py else load_literal_data_from_py
        )(path)  # type: ignore

    if any_load is not None:
        return any_load(path)

    if path.suffix == '.json':
        if keep_order:
            return json.load(
                path.open(), object_hook=collections.OrderedDict
            )

        return json.load(path.open())

    if path.suffix in ('.yaml', '.yml') and yaml_load is not None:
        return yaml_load(path.open())

    raise ValueError(f"Don't know how to load: {path!s}")


def each_data_under_dir(datadir: pathlib.Path,
                        pattern: str,
                        load_fn: typing.Optional[typing.Callable] = None,
                        safe: bool = True
                        ) -> typing.Iterator[datatypes.DataInfo]:
    """Load data from files under ``datadir`` match with ``pattern``."""
    if not datadir.is_dir():
        raise ValueError(f'Not a data dir: {datadir!s}')

    if load_fn:
        def _load(path, *_args, **_kwargs):
            """Call ``load_fn`` with only ``path`` argument."""
            return load_fn(path)
    else:
        _load = load_from_path  # type: ignore

    # Load data from files under ``datadir`` recursively.
    for path in sorted(datadir.glob(pattern)):
        if safe:
            try:
                data = _load(path)
            except (ValueError, RuntimeError) as exc:
                warnings.warn(str(exc))
        else:
            data = _load(path)

        yield datatypes.DataInfo(data=data, path=path, datadir=datadir)

# vim:sw=4:ts=4:et:
