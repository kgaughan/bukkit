#!/usr/bin/env python

from __future__ import with_statement

from setuptools import setup
from buildkit import *


META = get_metadata('bukkit/__init__.py')


setup(
    name='bukkit',
    version=META['version'],
    description='Keyed collections of token buckets.',
    long_description=read('README'),
    url='https://github.com/kgaughan/bukkit/',
    license='MIT',
    packages=['bukkit'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],

    author=META['author'],
    author_email=META['email']
)
