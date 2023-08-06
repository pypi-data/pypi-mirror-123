#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Plugin test cases #0."""
from . import constants, utils


def test_plugin_installed(pytestconfig):
    assert pytestconfig.pluginmanager.get_plugin(constants.PLUGIN_NAME)


def test_plugin(test_data):
    assert test_data
    assert len(test_data) == 1, test_data  # see tests/data/plugin/.

    basename = utils.get_basename(__file__)
    datadir = constants.DATADIR / basename
    subdirs = sorted(s for s in datadir.glob('*') if s.is_dir())

    for idx, data in enumerate(test_data):
        assert data
        assert len(data) == 2, data
        assert all(d.path for d in data), data
        assert all(d.data for d in data), data
        assert all(d.datadir == subdirs[idx] for d in data), data

    # data loaded from tests/data/plugin/20/input/00.py and
    # tests/data/plugin/20/expected/00.json should be same.
    assert test_data[0][0].data == test_data[0][1].data, test_data

# vim:sw=4:ts=4:et:
