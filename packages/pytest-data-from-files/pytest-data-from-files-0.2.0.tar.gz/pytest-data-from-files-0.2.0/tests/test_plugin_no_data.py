#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Plugin test cases #1."""


def test_plugin_with_no_data_case(test_data):
    assert not test_data, test_data

# vim:sw=4:ts=4:et:
