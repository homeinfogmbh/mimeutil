#! /usr/bin/env python3
"""Setup script."""

from setuptools import setup

setup(
    name='mimeutil',
    use_scm_version={
        "local_scheme": "node-and-timestamp"
    },
    setup_requires=['setuptools_scm'],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    install_requires=['python-magic'],
    py_modules=['mimeutil'],
    license='GPLv3',
    description='A MIME type and file extension library.'
)
