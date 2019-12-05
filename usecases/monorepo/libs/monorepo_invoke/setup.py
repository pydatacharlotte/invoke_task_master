#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="monorepo_invoke",
    version="0.1.0",
    description="monorepo invoke utilities",
    author="Rob Helgeson",
    author_email="RHelgeson@ATD-US.com",
    packages=find_packages(),
    install_requires=["invoke"],
)
