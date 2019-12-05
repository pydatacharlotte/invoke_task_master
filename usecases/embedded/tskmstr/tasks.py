""" A couple example subcommands for the create your own CLI example. """
from invoke import task


@task
def calculate_pi(context, digits=314):  # pylint: disable=unused-argument
    """ Sample subcommand 1. """
    print(f"Calculating pi to {digits} digits!")


@task
def start_server(context, server_name="devserver"):  # pylint: disable=unused-argument
    """ Sample subcommand 1. """
    print(f"Starting up {server_name}.")
