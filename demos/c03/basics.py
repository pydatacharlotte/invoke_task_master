"""
Basic examples from Invoke: How to be a @task Master.

# The `@task` decorator

The `@task` decorator will add your functions to the list of available
    invoke tasks that can be executed from the commandline.

## Things to see:
1. `inv --list` will show all of the tasks defined
    ```python
    $ inv --list
    Available tasks:

    hello-world
    ```

    Take special note here that the underscore was converted to a hyphen
    invoke bridges the python world where so called "snake_case" is the norm
    and the command line world where so called "kabob-case" is the norm, so
    it implicitly converts underscores into hyphens in commands and options.
    This can be disabled in configuration by setting the 'auto_dash_names'
    setting to false.

2. `inv hello-world --help` will show all of the information that invoke
knows about your task, including the docstring and the options, if any.

3. `inv hello-world` will run the python and produce the expected output.

That's it. It really is that simple to get started using invoke. However
there are many more features that invoke exposes that we will explore in
the next few demos.

"""

from invoke import task


@task
def hello_world(context):  # pylint: disable=unused-argument
    """ The obligatory first example. """

    print("Hello world!")
