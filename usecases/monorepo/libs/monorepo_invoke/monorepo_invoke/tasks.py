""" Utility tasks for all the monorepo applications. """
import os

from dotenv import dotenv_values
from invoke import task

from tmp_copy import tmp_copy

# APP_NAME is the name of the  the root of your project's folder.
# It will be defined by calling init_monorepo_tasks()
#
APP_NAME = "DEFINE_ME - call init_monorepo_tasks()"

# Typically APP_DIR is the root of your project's folder.
# Often it's defined as: APP_DIR = os.path.realpath(os.path.dirname(__file__))
# It will be defined by calling init_monorepo_tasks()
#
APP_DIR = f"./apps/{APP_NAME}"
BASE_DIR = os.path.realpath(os.path.join(APP_DIR, "../.."))


# IMAGE_NAME is the name of the container and service on app engine.
# It will be defined by calling init_monorepo_tasks()
#
IMAGE_NAME = "DEFINE_ME - call init_monorepo_tasks()"

PROJECT = "APROJECTNAME"
GCR_HOSTNAME = "us.gcr.io"

TASKS_INITIALIZED = False


def init_monorepo_tasks(
    app_name: str,
    image_name: str,
    project: str = "APROJECTNAME",
    gcr_hostname: str = "us.gcr.io",
) -> None:
    """ Initialize some global variables. """

    global APP_NAME, IMAGE_NAME, APP_DIR, BASE_DIR  # pylint: disable=global-statement
    global PROJECT, GCR_HOSTNAME, TASKS_INITIALIZED  # pylint: disable=global-statement

    APP_NAME = app_name
    IMAGE_NAME = image_name

    APP_DIR = f"./apps/{APP_NAME}"
    BASE_DIR = os.path.realpath(os.path.join(APP_DIR, "../.."))

    PROJECT = project
    GCR_HOSTNAME = gcr_hostname

    TASKS_INITIALIZED = True


def get_app_name():
    """ Getter for invoke global. """
    if not TASKS_INITIALIZED:
        raise SyntaxError("You must call init_monorepo_tasks() before using this task.")

    global APP_NAME  # pylint: disable=global-statement
    return APP_NAME


def get_image_name():
    """ Getter for invoke global. """
    if not TASKS_INITIALIZED:
        raise SyntaxError("You must call init_monorepo_tasks() before using this task.")

    global IMAGE_NAME  # pylint: disable=global-statement
    return IMAGE_NAME


def get_app_dir():
    """ Getter for invoke global. """
    if not TASKS_INITIALIZED:
        raise SyntaxError("You must call init_monorepo_tasks() before using this task.")

    global APP_DIR  # pylint: disable=global-statement
    return APP_DIR


def get_base_dir():
    """ Getter for invoke global. """
    if not TASKS_INITIALIZED:
        raise SyntaxError("You must call init_monorepo_tasks() before using this task.")

    global BASE_DIR  # pylint: disable=global-statement
    return BASE_DIR


def get_project():
    """ Getter for invoke global. """
    if not TASKS_INITIALIZED:
        raise SyntaxError("You must call init_monorepo_tasks() before using this task.")

    global PROJECT  # pylint: disable=global-statement
    return PROJECT


def get_gcr_hostname():
    """ Getter for invoke global. """
    if not TASKS_INITIALIZED:
        raise SyntaxError("You must call init_monorepo_tasks() before using this task.")

    global GCR_HOSTNAME  # pylint: disable=global-statement
    return GCR_HOSTNAME


def validate_env(env: str) -> bool:
    """ Ensure that the environment string is valid. """

    if env in ("local", "dev", "prod"):
        return True

    raise Exception(
        f"env: {env} is invalid. env must be either 'local', 'dev', or 'prod'"
    )


def get_ng_build_env(env: str) -> str:
    """ Translate the env string for angular that uses a more verbose string. """
    return "production" if env == "prod" else ""


def get_default_secrets_path(env: str) -> str:
    """ Default value for the secrets file. """
    return f"{get_app_dir()}/something.secret.{env}.env"


def create_deploy_yaml_file(
    yaml_file_path: str,
    env: bool,
    secrets_file_path: str,
    service_name: str,
    cloud_sql_instances: str,
) -> str:
    """ Merge env vars to app yaml. """
    from ruamel.yaml import YAML, util

    yaml = YAML()

    yaml_file_name = yaml_file_path.split("/")[-1]
    file_dir = "/".join(yaml_file_path.split("/")[:-1])

    # Open and read base app-engine.yaml file
    config = util.load_yaml_guess_indent(open(yaml_file_path))[0]

    if service_name:
        print(f"Using service_name: {service_name}")
        config["service"] = service_name
    else:
        print(f"Using service_name: {config['service']}")

    # Open and read secret env variables
    if secrets_file_path is None:
        secrets_file_path = get_default_secrets_path(env)

    print(f"Using secrets_file_path: {secrets_file_path}")
    env_vars = dotenv_values(secrets_file_path)

    # update yaml in memory before writing new file with changes
    config["env_variables"] = (
        {} if "env_variables" not in config else config["env_variables"]
    )

    for key, val in env_vars.items():
        config["env_variables"][key] = val

    # If cloud_sql_instances provided, set beta_settings to it.
    if cloud_sql_instances:
        config["beta_settings"]["cloud_sql_instances"] = cloud_sql_instances

    deploy_file_path = f"{file_dir}/deploy-{yaml_file_name}"

    # write to new file the updated yaml file
    with open(deploy_file_path, "w") as out_file:
        yaml.dump(config, out_file)

    return deploy_file_path


@task
def clean(ctx):
    """ Remove intermediate files. """

    ctx.run("find . -type f -name '*.pyc' -delete", echo=True)
    ctx.run("find . -type f -name '*.log' -delete", echo=True)

    print("Cleaning Finished!")


@task
def install(ctx):
    """ Install dependencies. """

    ctx.run("pip install -r requirements.txt", echo=True)

    print("Install Finished!")


@task
def test(ctx):
    """ Run tests. """

    ctx.run("python manage.py test", echo=True)


@task
def run(ctx):
    """ Run the application. """

    ctx.run("python manage.py run", echo=True)


@task
def seed(ctx):
    """ Seed the Database. """

    ctx.run("python manage.py seed_db", echo=True)


@task
def docker_build(ctx, project=PROJECT, env="local"):
    """ Build the application container with docker. """

    with ctx.cd(get_base_dir()), tmp_copy(f"{get_app_dir()}/Dockerfile"), tmp_copy(
        f"{get_app_dir()}/docker-compose.yaml"
    ):
        validate_env(env)
        ng_build_env = get_ng_build_env(env)

        ctx.run(
            f"export ENV={env} && export GCP_PROJECT_ID={project} && "
            + f"export NG_BUILD_ENV={ng_build_env} && docker-compose build",
            echo=True,
        )


@task
def docker_run(ctx, project=PROJECT, env="local"):
    """ Run the application container with docker. """
    with ctx.cd(get_base_dir()), tmp_copy(f"{get_app_dir()}/docker-compose.yaml"):
        validate_env(env)
        ng_build_env = get_ng_build_env(env)

        try:
            ctx.run(
                f"export ENV={env} && export GCP_PROJECT_ID={project} && "
                + f"export NG_BUILD_ENV={ng_build_env} && docker-compose up"
            )

        finally:
            ctx.run(
                f"export ENV={env} && export GCP_PROJECT_ID={project} && "
                + f"docker-compose down"
            )


@task
def docker_push(ctx, project=PROJECT):
    """ Push the application container to the container registry with docker. """

    ctx.run(
        f"docker push {get_gcr_hostname()}/{project}/discoe/{get_image_name()}",
        echo=True,
    )


@task
def deploy(
    ctx,
    project=PROJECT,
    build=True,
    promote=False,
    secrets_file_path=None,
    service_name=None,
    with_cron=False,
    cloud_sql_instances=None,
):
    """ Deploy the container to GCP. """

    env = "prod"
    deploy_yaml = create_deploy_yaml_file(
        f"{get_app_dir()}/app-engine.yaml",
        env,
        secrets_file_path,
        service_name,
        cloud_sql_instances,
    )
    with tmp_copy(deploy_yaml):
        if build:
            docker_build(ctx, project, env)
            docker_push(ctx, project)

        image_url = f"{get_gcr_hostname()}/{project}/discoe/{get_image_name()}"
        print(f"image_url: {image_url}")

        promote_flag = "--promote" if promote else "--no-promote"
        print(f"promote_flag: {promote_flag}")

        ctx.cd(os.path.join(get_app_dir(), ".."))

        ctx.run(
            f"gcloud app deploy --project {project} "
            + f"--image-url={image_url} {promote_flag} {deploy_yaml}",
            echo=True,
        )

        if with_cron:
            cron_deploy(ctx, project)


@task
def cron_deploy(ctx, project=PROJECT, cron_file=f"./cron.yaml"):
    """ Deploy the cron file to GCP. """

    if os.path.isfile(cron_file):
        with ctx.cd(get_base_dir()):
            ctx.run(f"gcloud app deploy --project {project} {cron_file}", echo=True)
    else:
        print("cron file not found. Skipping cron deployment.")
