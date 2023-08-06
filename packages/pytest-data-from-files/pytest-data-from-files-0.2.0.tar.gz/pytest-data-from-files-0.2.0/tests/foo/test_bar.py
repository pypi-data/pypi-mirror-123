#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""foo/bar test cases."""
import json
import pathlib

from .. import constants, utils


def test_foo_bar(test_data):
    assert test_data
    assert len(test_data) == 1, test_data  # see tests/data/foo/bar/.

    basename = utils.get_basename(__file__)
    parent = pathlib.Path(__file__).parent

    datadir = constants.DATADIR / parent.name / basename
    ref_paths = sorted(p for p in datadir.glob('**/*.*') if p.is_file())

    for data_per_subdir in test_data:
        assert data_per_subdir
        assert len(data_per_subdir) == 2, data_per_subdir
        assert all(d.path and d.path in ref_paths for d
                   in data_per_subdir), data_per_subdir
        assert all(d.data for d in data_per_subdir), data_per_subdir

    # data loaded from tests/data/foo/bar/input.py and
    # tests/data/foo/bar/expected.json should be same.
    assert test_data[0][0].data == test_data[0][1].data, test_data

    # One more check.
    ref = json.load((constants.DATADIR / 'foo/bar/10/expected.json').open())
    assert test_data[0][0].data == ref

    paths = sorted(utils.concat((d.path for d in data) for data in test_data))
    assert paths == ref_paths

# vim:sw=4:ts=4:et:
