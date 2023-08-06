#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Fixtures to load test data."""
import pytest

from . import constants, loader, modinfo


@pytest.fixture(scope='module')
def test_data_info(request: pytest.FixtureRequest):
    """Fixture provides some path info of the target module."""
    return modinfo.get_test_data_info_for_target(request)


# .. note:: To disable pylint's warning about the reuse of fixture.
# pylint: disable=redefined-outer-name
@pytest.fixture
def test_data(test_data_info, pytestconfig):
    """Fixture provides test data loaded from files automatically."""
    data_pattern = pytestconfig.getoption(constants.OPT_DATA_PATTERN)

    if test_data_info.subdirs:
        return list(
            list(loader.each_data_under_dir(
                test_data_info.datadir / subdir, data_pattern
            ))
            for subdir in test_data_info.subdirs
        )

    return list(
        loader.each_data_under_dir(test_data_info.datadir, data_pattern)
    )

# vim:sw=4:ts=4:et:
