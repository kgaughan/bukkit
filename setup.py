#!/usr/bin/env python

from distutils.core import setup
import bukkit

setup(
    name='bukkit',
    version=bukkit.__version__,
    description='Keyed collections of token buckets.',
    long_description=open('README').read(),
    url='https://github.com/kgaughan/bukkit/',
    license='MIT',
    py_modules=['bukkit'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],

    author=bukkit.__author__,
    author_email=bukkit.__email__
)
