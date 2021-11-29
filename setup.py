#! /usr/bin/env python3

from setuptools import setup

setup(
    name='mimeutil',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info at homeinfo dot de>',
    maintainer='Richard Neumann',
    maintainer_email='<r dot neumann at homeinfo priod de>',
    py_modules=['mimeutil'],
    license='GPLv3',
    description='A MIME type and file extension library.'
)
