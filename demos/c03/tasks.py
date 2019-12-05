"""
Demo how to use namespaces and use pre and post actions, to manage
large task sets and dependency management.

# Namespaces

## Things to see:
1. If you need to name your function one thing but would like the task
to be called something else, use the `name` parameter of the task itself.

2. Invoke creates a default unnamed namespace, and adds all tasks in
tasks.py to it.

3. To import other tasks into the local namespace, create a namespace
named with one of the "magic values", either `namespace` or `ns` by
calling `Collection()`. This will give you a handle to a new, empty
namespace. From there, you can use `namespace.add_task()` to attach
tasks to it.

4. To avoid namespace collisions, use the `name` parameter of `add_task()`
to rename the new task.

5. Namespaces can be nested to arbitrary depth by calling
`namespace.add_collection('name', other_namespace)`.

# Dependencies

1. To run a task as a dependency of another task, pass the dependency
to the `@task()` decorator as an argument called `pre`, or as the first
positional argument. Similarly, to run a task after another task, pass
the dependency to the `@task()` decorator as an argument called `post`,
or as the second positional argument.

2. Note that parameters can be passed to dependencies with an advanced
syntax, `pre=[call(pre_task_name, arg='value')]`

3. Tasks will not run more than one time in a single run of a dependency
chain. This default is overridden by using the `invoke` command line
option, `--no-dedupe`.

"""

from invoke import task
from invoke.collection import Collection

import basics  # pylint: disable=unused-import
import dependencies  # pylint: disable=unused-import
import params  # pylint: disable=unused-import


@task
def demo(context):  # pylint: disable=unused-argument
    """ This is a test global task. """

    print("I am a global task.")


@task(name="omed")
def _demo(context):  # pylint: disable=unused-argument
    """ This task shows how to change the task name. """

    print("I am named _demo but my task is called omed.")


# namespace = Collection()  # pylint: disable=invalid-name
# namespace.add_task(demo)
# namespace.add_task(_demo)
# namespace.add_task(dependencies.demo)
# namespace.add_task(dependencies.demo, name="dependenciesdemo")

# Magic value here, can be called ns or namespace
#
namespace = Collection(basics, params, dependencies)  # pylint: disable=invalid-name
namespace.add_task(demo)
namespace.add_task(_demo)
