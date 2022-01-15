#! /usr/bin/env python3

from setuptools import setup

setup(
    name='mimeutil',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=['python-magic'],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info@homeinfo.de>',
    maintainer='Richard Neumann',
    maintainer_email='<r.neumann@homeinfo.de>',
    py_modules=['mimeutil'],
    license='GPLv3',
    description='A MIME type and file extension library.'
)
