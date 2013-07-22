#!/usr/bin/env python

from __future__ import with_statement

import os.path
import sys

from setuptools import setup


def read(*filenames):
    """Read files relative to the executable."""
    files = []
    for filename in filenames:
        full_path = os.path.join(os.path.dirname(sys.argv[0]), filename)
        with open(full_path, 'r') as fh:
            files.append(fh.read())
    return "\n\n".join(files)


setup(
    name='bukkit',
    version='0.1.0',
    description='Keyed collections of token buckets.',
    long_description=read('README', 'ChangeLog'),
    url='https://github.com/kgaughan/bukkit/',
    license='MIT',
    packages=['bukkit'],

    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ),

    author='Keith Gaughan',
    author_email='k@stereochro.me',
)
