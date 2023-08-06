#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
"""Some internal data types."""
import pathlib
import typing


DataT = typing.Optional[typing.Any]


class ModuleInfo(typing.NamedTuple):
    """A namedtuple object keeps info of the test target module."""

    root: pathlib.Path
    datadir: pathlib.Path
    subdirs: typing.List[str]


class DataInfo(typing.NamedTuple):
    """A namedtuple object keeps data and its related info like path."""

    data: DataT
    path: pathlib.Path
    datadir: pathlib.Path

# vim:sw=4:ts=4:et:
