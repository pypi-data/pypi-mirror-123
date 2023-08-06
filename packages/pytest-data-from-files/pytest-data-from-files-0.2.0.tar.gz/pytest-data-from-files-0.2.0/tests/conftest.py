#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""conftest.py to load data_from_files.*."""
from . import constants


pytest_plugins = [constants.PLUGIN_NAME]

# vim:sw=4:ts=4:et:
