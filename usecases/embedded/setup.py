""" Make the entrypoint 'tskmstr' """

from setuptools import setup

setup(
    name="tskmstr",
    author="Rob Helgeson",
    author_email="RHelgeson@atd-us.com",
    version="50.0.0",
    packages=["tskmstr"],
    install_requires=["invoke"],
    entry_points={"console_scripts": ["tskmstr = tskmstr.main:program.run"]},
)
