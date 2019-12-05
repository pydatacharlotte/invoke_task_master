"""
Invoke tasks for showing off the context argument and how to work
with options.

# The `context` argument

The `context` argument is used to keep track of state across an `invoke`
session. This allows all tasks executed to have consistancy. It is easy
to forget this paramater, which results in what looks like the intended
first parameter going away, because it is actually being set by invoke
as the context parameter. When debugging, check here first.

## Things to see:
1. `context` is the first argument to all `@task` decorated functions
    it is often shortened to `ctx` or just `c`, but in the examples
    here they are left as `context`.

2. 'context' itself has a context manager for changing directories,
    and running command lines from within that dir.
    ```python
    with context.cd("../c01"):
        context.run("ls -rt")
        context.run("cat "$(ls -rt | tail -n1)")
    ```

# Command line options

Invoke does a lot when it comes to options. The parsing library is very
rich, and even works with datatypes other than strings. Invoke uses the
datatype from the default arg to determine the datatype of the variable
if there is no default, string is used.

## Things to see:

1. Arguments, like tasks, are converted from "snake_case" to "kabob-case"
automatically.

2. A wide variety of argument types can be exposed as command line options.
Strings, numbers, booleans and lists are all available.

3. Types of the arguments are set by the defaults in the function signature.
Be especially wary of using numeric types. If a string is passed and it
cannot be parsed as a numeric, an exception will be raised.

4. Booleans are treated specially. For booleans that default to `True`, two
options are created. For example: with an argument named `foo` you will get
`--foo` as well as a `--no-foo` option. For default `False` booleans, only
one option, `--foo` will be generated.

"""

from invoke import task


@task(help={"path": "directory to look in"})
def cat_c01_latest(context, path="../c01"):
    """ Use context to show the contents of the most recently changed
    file in the specified directory. """

    with context.cd(path):
        context.run("ls -rt")
        context.run('cat "$(ls -rt | tail -n1)"')


@task(help={"name": "The name to greet"})
def greet(context, name="human"):  # pylint: disable=unused-argument
    """ First use of parameters. """

    print(f"Pleasure to meet you, {name}.")


@task
def showoff_greet(context):
    """ Show all the different ways that you can set an option. """

    context.run("inv greet --name Rob", echo=True)
    context.run("inv greet --name=Rob", echo=True)
    context.run("inv greet -n Rob", echo=True)
    context.run("inv greet -n=Rob", echo=True)
    context.run("inv greet -nRob", echo=True)

    try:
        context.run("inv greet Rob", echo=True)
    except Exception:  # pylint: disable=broad-except
        print("That didn't work!")

    try:
        context.run("inv greet --nameRob", echo=True)
    except Exception:  # pylint: disable=broad-except
        print("That didn't work!")


@task(
    help={"num": "A param typed as a number", "string": "A param typed as a string"},
    iterable=["a_list"],
    incrementable=["verbose"],
)
def params(
    context,
    a_list,
    verbose=0,
    num=42,
    string="Hi there!",
    is_debug=True,
    is_admin=False,
):
    """ A task that shows off how Invoke defaults datatypes. """

    print(f"The value of 'a_list' is {a_list}. The type is {type(a_list)}")
    print(f"The value of 'verbose' is {verbose}. The type is {type(verbose)}")
    print(f"The value of 'num' is {num}. The type is {type(num)}")
    print(f"The value of 'string' is {string}. The type is {type(string)}")
    print(f"The value of 'is_debug' is {is_debug}. The type is {type(is_debug)}")
    print(f"The value of 'is_admin' is {is_admin}. The type is {type(is_admin)}")


@task
def showoff_params(context):
    """ Show all the different option types. """

    context.run("inv params --a-list Foo --a-list bar", echo=True)
    context.run("inv params -vvvvvvv", echo=True)

    context.run("inv params -n100", echo=True)

    try:
        context.run("inv params --num 'a string?'", echo=True)
    except Exception:  # pylint: disable=broad-except
        print("That didn't work!")

    context.run("inv params --is-debug", echo=True)
    context.run("inv params --no-is-debug", echo=True)

    context.run("inv params --is-admin", echo=True)
    context.run("inv params --no-is-admin", echo=True)
