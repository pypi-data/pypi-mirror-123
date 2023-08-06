Overview
==========

.. .. image:: https://img.shields.io/pypi/v/pytest_data_from_files.svg
   :target: https://pypi.python.org/pypi/pytest_data_from_files/
   :alt: [Latest Version]

.. .. image:: https://img.shields.io/pypi/pyversions/pytest_data_from_files.svg
   :target: https://pypi.python.org/pypi/pytest_data_from_files/
   :alt: [Python versions]

.. .. image:: https://img.shields.io/pypi/l/pytest_data_from_files.svg
   :target: https://pypi.python.org/pypi/pytest_data_from_files/
   :alt: MIT License

.. image:: https://github.com/ssato/pytest-data-from-files/workflows/Tests/badge.svg
   :target: https://github.com/ssato/pytest-data-from-files/actions?query=workflow%3ATests
   :alt: [Github Actions: Test status]

A pytest plugin to provide fixtures to load test data from files automatically.

Usage
======

Fixtures
----------

This plugin provides following fixtures for each test modules.

test_data_info
^^^^^^^^^^^^^^^^

*test_data_info* provides a namedtuple object, `data_from_files.ModuleInfo`,
has the following values for each test modules.

- root: test root dir, <package_dir>/tests/ by default and is configurable with --test-root (test_root) option.
- datadir: test data dir using the fixture will be searched under <root>/<test_data_dirname>/,  where test_data_dirname is configurable with --test-data-dirname option.

  - if the test code using the fixture is tests/test_foo.py, then datadir becomes tests/data/foo/
  - if the test code using the fixture is tests/foo/bar/test_baz.py, then datadir becomes tests/data/foo/bar/baz

- subdirs: names of sub dirs relative to datadir if such dirs exist.

test_data
^^^^^^^^^^

*test_data* provides a list of or a list of lists of namedtuple objects,
`data_from_files.DataInfo`, has the following values.

- data: data loaded from a file <path> under <datadir>
- path: a file path contains the data
- datadir: dir contains the test data file

Options
---------------

- --test-root: test root dir where test data are seached [<package_dir>/tests]
- --test-data-dirname: test data dir name [data]
- --test-data-pattern: test data file path pattern relative to datadir [\*\*/\*.\*]

Examples
-----------

- tests/test_plugin.py and test data under tests/data/plugin/
- tests/test_plugin_no_data.py and test data under tests/data/plugin_no_data
- tests/foo/test_bar.py and test data under tests/data/foo/bar

Installation
==============

Requirements
---------------

- pytest obviously
- PyYAML [#]_ is optionally required to load data from YAML files
- anyconfig [#]_ is optionally required to load data in formats anyconfig and/or its plugins support.

.. [#] PyYAML: https://pyyaml.org
.. [#] anyconfig: https://github.com/ssato/python-anyconfig

How to install
----------------

- PyPI::

    pip install pytest_data_from_files

- From git repo::

    pip install git+https://github.com/ssato/pytest-data-from-files

- Build wheel and install it::

    tox -e dists && pip install dist/pytest_data_from_files-*.whl

.. vim:sw=2:ts=2:et:
