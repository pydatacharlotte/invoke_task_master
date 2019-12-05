"""
A simple set of tasks to demonstrate execution from within a
docker container.
"""

from invoke import task


@task
def pipeline_part_one(ctx):  # pylint: disable=unused-argument
    """ Thing one. """
    print("Pipeline one started.")


@task
def pipeline_part_two(ctx):  # pylint: disable=unused-argument
    """ Thing two. """
    print("Pipeline two started.")
