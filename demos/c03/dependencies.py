"""
A demo of recursive tasks and dependencies from the invoke documentation.
http://docs.pyinvoke.org/en/1.3/concepts/invoking-tasks.html#recursive-chained-pre-post-tasks
"""

from invoke import task


@task
def clean_html(c):  # pylint: disable=unused-argument, invalid-name
    """ Example task from the invoke documentation. """
    print("Cleaning HTML")


@task
def clean_tgz(c):  # pylint: disable=unused-argument, invalid-name
    """ Example task from the invoke documentation. """
    print("Cleaning .tar.gz files")


@task(clean_html, clean_tgz)
def clean(c):  # pylint: disable=unused-argument, invalid-name
    """ Example task from the invoke documentation. """
    print("Cleaned everything")


@task
def makedirs(c):  # pylint: disable=unused-argument, invalid-name
    """ Example task from the invoke documentation. """
    print("Making directories")


@task(clean, makedirs)
def build(c):  # pylint: disable=unused-argument, invalid-name
    """ Example task from the invoke documentation. """
    print("Building")


@task(build)
def deploy(c):  # pylint: disable=unused-argument, invalid-name
    """ Example task from the invoke documentation. """
    print("Deploying")


@task
def demo(c):  # pylint: disable=unused-argument, invalid-name
    """ Example showing task deduplicaton. """

    c.run("inv dependencies.build dependencies.package", echo=True)
    c.run("inv --no-dedupe dependencies.build dependencies.package", echo=True)


@task(build)
def package(c):
    """ Example task from the invoke documentation. """
    print("Packaging")
