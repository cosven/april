#!/usr/bin/env python

from setuptools import setup


setup(
    name='april',
    version='2.0.1',
    description='simplified obj',
    author='Cosven',
    author_email='cosven.yin@gmail.com',
    py_modules=['april'],
    url='https://github.com/cosven/april',
    keywords=['struct', 'model'],
    classifiers=(
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ),
    tests_require=['pytest'],
    entry_points={
        'console_scripts': []
        },
    )
