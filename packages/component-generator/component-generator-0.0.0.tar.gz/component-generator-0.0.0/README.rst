========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-component-generator/badge/?style=flat
    :target: https://python-component-generator.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/onna/python-component-generator.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/onna/python-component-generator

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/onna/python-component-generator?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/onna/python-component-generator

.. |requires| image:: https://requires.io/github/onna/python-component-generator/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/onna/python-component-generator/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/onna/python-component-generator/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/onna/python-component-generator

.. |version| image:: https://img.shields.io/pypi/v/component-generator.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/component-generator

.. |wheel| image:: https://img.shields.io/pypi/wheel/component-generator.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/component-generator

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/component-generator.svg
    :alt: Supported versions
    :target: https://pypi.org/project/component-generator

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/component-generator.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/component-generator

.. |commits-since| image:: https://img.shields.io/github/commits-since/onna/python-component-generator/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/onna/python-component-generator/compare/v0.0.0...master



.. end-badges

Generate backend components quickly

* Free software: BSD 2-Clause License

Installation
============

::

    pip install component-generator

You can also install the in-development version with::

    pip install https://github.com/onna/python-component-generator/archive/master.zip


Documentation
=============


https://python-component-generator.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
