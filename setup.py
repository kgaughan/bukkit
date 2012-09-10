#!/usr/bin/env python

from __future__ import with_statement

from distutils.core import setup
import re


def read(filename):
    with open(filename, 'r') as fh:
        return fh.read()


def get_metadata(module_path):
    """Extract the metadata from a module file."""
    matches = re.finditer(
        r"^__(\w+?)__ *= *'(.*?)'$",
        read(module_path),
        re.MULTILINE)
    return dict(
        (match.group(1), match.group(2).decode('unicode_escape'))
        for match in matches)


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
