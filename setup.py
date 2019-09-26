#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='uninews',
    version='latest',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info at homeinfo dot de>',
    maintainer='Richard Neumann',
    maintainer_email='<r dot neumann at homeinfo priod de>',
    requires=['newslib', 'his'],
    packages=['uninews'],
    description='Multi-source news API.')
