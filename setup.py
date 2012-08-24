#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='bukkit',
    version='0.1.0',
    description='Keyed collections of token buckets.',
    long_description=open('README').read(),
    url='https://github.com/kgaughan/bukkit/',
    license='MIT',
    packages=find_packages(exclude='tests'),
    zip_safe=True,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],

    author='Keith Gaughan',
    author_email='k@stereochro.me'
)
