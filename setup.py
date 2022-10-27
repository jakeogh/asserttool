# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

import fastentrypoints

dependencies = ["epprint @ git+https://git@github.com/jakeogh/epprint"]

config = {
    "version": "0.1",
    "name": "asserttool",
    "url": "https://github.com/jakeogh/asserttool",
    "license": "ISC",
    "author": "Justin Keogh",
    "author_email": "github.com@v6y.net",
    "description": "common programming functions, similar to assert",
    "long_description": __doc__,
    "packages": find_packages(exclude=["tests"]),
    "package_data": {"asserttool": ["py.typed"]},
    "include_package_data": True,
    "zip_safe": False,
    "platforms": "any",
    "install_requires": dependencies,
}

setup(**config)
