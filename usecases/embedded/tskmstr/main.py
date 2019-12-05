"""
    Show what configuration is necessary to build your own CLI.
    by setting the namespace in the program definition we override
    the defaults present in invoke.
"""
from invoke import Collection, Program

from tskmstr import tasks

program = Program(namespace=Collection.from_module(tasks), version="50.0.0")
