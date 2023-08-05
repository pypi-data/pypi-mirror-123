#!/usr/bin/env python

"""The setup script."""

import codecs
import os

from setuptools import setup, find_namespace_packages


###################################################################

DESCRIPTION="A module that exposes a function to get an instance of a driver for a specific interface (module)"
KEYWORDS = [
    'driver.interface',
]
###################################################################

setup(
    name="driver.interface",
    author="Marco Masetti",
    author_email="grubert65@gmail.com",
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    long_description_content_type="text/x-rst",
    license="BSD",
    url="https://github.com/grubert65/driver.interface",
    keywords=KEYWORDS,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[],
    include_package_data=True,
    packages=find_namespace_packages(include=['driver.interface', 'driver.interface.*']),
    zip_safe=False,
    version="0.1.0",
)
