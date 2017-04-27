#!/usr/bin/env python3

from setuptools import setup

import april


setup(
    name='april',
    version=april.__version__,
    description='simplified data deserialization',
    author='Cosven',
    author_email='cosven.yin@gmail.com',
    packages=['april'],
    package_data={
        '': []
        },
    url='https://github.com/cosven/april',
    keywords=['python', 'deserialization', 'serialization'],
    classifiers=(
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        ),
    install_requires=[
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': []
        },
    )
