#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Setup dot py."""
from __future__ import absolute_import, print_function

# import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


def read(*names, **kwargs):
    """Read description files."""
    path = join(dirname(__file__), *names)
    with open(path, encoding=kwargs.get("encoding", "utf8")) as fh:
        return fh.read()


long_description = "{}".format(
    read("README.md"),
)

setup(
    name="platform-tools",
    description="A collection of tools for working with GCP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    author="TreeHouse",
    author_email="dev@treehouse.nl",
    url="https://github.com/treehouselabs/platform-tools",
    packages=find_packages("."),
    package_dir={"": "."},
    py_modules=[splitext(basename(i))[0] for i in glob("treehouse/*.py")],
    version="0.2",
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Programming Language :: Python :: 3.10",
    ],
    keywords=[],
    python_requires=">=3.8",
    install_requires=[
        "dask",
        "google-cloud-dataproc",
        "google-cloud-firestore",
        "google-cloud-pubsub",
        "google-cloud-secret-manager",
        "google-cloud-storage",
        "pandas",
        "gcsfs",
        "mysqlclient",
        "paramiko",
        "pg8000",
        "pyarrow",
        "pyspark",
        "PyMySQL",
        "sshtunnel",
        "SQLAlchemy<=2.0",
    ],
)
