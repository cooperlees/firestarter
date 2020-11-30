#!/usr/bin/env python3
# Copyright (c) 2014-present, Facebook, Inc.

from setuptools import setup


setup(
    name="firestarter",
    version="6.9",
    description="Simple HTTP frontend for turning my fireplace on and off",
    packages=["firestarter"],
    package_dir={"": "src"},
    url="http://github.com/cooperlees/firestarter/",
    author="Cooper Lees",
    author_email="me@cooperlees.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.8",
    install_requires=[
        "RPi.GPIO",
        "aiohttp",
        "basicauth",
        "gunicorn",
        "uvloop",
    ],
)
