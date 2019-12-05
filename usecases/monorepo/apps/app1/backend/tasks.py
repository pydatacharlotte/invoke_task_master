""" Utility tasks associated with the current application """
import os
import time

from atdcoe_invoke import (
    clean,
    cron_deploy,
    deploy,
    docker_build,
    docker_push,
    docker_run,
    init_atdcoe_tasks,
    install,
    run,
    seed,
    test,
)
from invoke import task

APP_NAME = "app1"

init_atdcoe_tasks("app1", "app1")


@task
def analyze_bundle(ctx, prod=True):
    """Analyze Angular bundle output"""
    ctx.run(
        f"ng build --project=app1 {'--prod' if prod else ''} --stats-json",
        echo=True,
        pty=True,
    )
    ctx.run(
        f"./node_modules/.bin/webpack-bundle-analyzer dist/apps/app1/stats.json",
        echo=True,
        pty=True,
    )


@task
def dev_setup(ctx):
    """Install Requirements for project"""

    ctx.run("pip install -r {TASK_DIR}/requirements.txt")


@task
def start_fe(ctx, port="4200", prod=False):
    prod_flag = "--prod=true" if prod else ""
    ctx.run(
        f"""ng serve --port {port} {prod_flag} --project={APP_NAME} """,
        pty=True,
        echo=True,
    )


@task
def start_local_pg(ctx):
    ctx.run(
        f"docker-compose -f {APP_DIR}/docker-compose-test.yaml up -d",
        pty=True,
        echo=True,
    )
    time.sleep(3)


@task
def stop_local_pg(ctx):
    ctx.run(
        f"docker-compose -f {APP_DIR}/docker-compose-test.yaml stop",
        pty=True,
        echo=True,
    )


@task
def destroy_local_pg(ctx):
    ctx.run(
        f"docker-compose -f {APP_DIR}/docker-compose-test.yaml down",
        pty=True,
        echo=True,
    )


@task
def start_be(ctx, wsgi_server=False, config_name="dev", host="127.0.0.1"):
    """Start the backend as a dev server or production ready gunicorn server"""
    if config_name == "test":
        start_local_pg(ctx)

    if wsgi_server:
        with ctx.cd(TASK_DIR):
            ctx.run(
                f"""gunicorn --bind {host}:5000 --workers 2 "app:create_app('{config_name}')" """,
                pty=True,
                echo=True,
            )
        return

    ctx.run(
        f"""
        export FLASK_ENV=development &&
        export FLASK_APP="{TASK_DIR}/app:create_app('{config_name}')" &&
        flask run --host={host}
        """,
        pty=True,
        echo=True,
    )


@task
def init_db(ctx, config_name="dev"):
    """Initialize Database"""
    from app import db, create_app
    from task_util.seed_util import drop_app_tables

    print("Config Name:", config_name)

    if config_name == "test":
        start_local_pg(ctx)

    app = create_app(config_name)

    with app.app_context():
        db.session.execute("CREATE SCHEMA IF NOT EXISTS a;")
        db.session.execute("CREATE SCHEMA IF NOT EXISTS b;")
        db.session.execute("CREATE SCHEMA IF NOT EXISTS c;")
        db.session.execute("CREATE SCHEMA IF NOT EXISTS d;")

        db.session.commit()

        if config_name == "test":
            db.drop_all(app=app)
        else:
            drop_app_tables(db.engine)

        db.create_all(app=app)


@task
def seed_db(ctx, config_name="dev"):
    """Initialize Database"""
    from app import db, create_app, guard
    from task_util.seed_util import (
        seed_user,
        seed_entity,
        seed_styles,
        seed_org_units,
        set_app_user_perms,
    )

    A_DATA: str = "seed_data/common_A_t.csv"
    B_DATA: str = "seed_data/common_B_t.csv"
    C_DATA: str = "seed_data/common_C_t.csv"

    print("Config Name:", config_name)

    if config_name == "test":
        start_local_pg(ctx)

    app = create_app(config_name)

    with app.app_context():
        # Seed A
        seed_entity(db, "A", A_DATA)
        # Seed B
        seed_entity(db, "B", B_DATA)
        # Seed C
        seed_entity(db, "C", C_DATA)

        set_app_user_perms(db)


@task
def test_be(ctx):
    """Test Python Backend"""
    ctx.run(f"pytest {APP_DIR}/backend", pty=True)


@task
def mypy(ctx):
    """Run MyPy linting on app1"""
    ctx.run(f"mypy {APP_DIR}/backend/app --ignore-missing-imports", pty=True)


@task
def pylint(ctx):
    """Run Pylint on app1"""
    ctx.run(f"pylint {APP_DIR}/backend/app", pty=True)


@task
def test_all(ctx):
    """Run all maintenance testing for app1"""
    print("Backend Testing...")
    test_be(ctx)
    print("mypy...")
    mypy(ctx)
    print("pylint...")
    pylint(ctx)


@task
def ssh(ctx):
    """Get the ssh command to log into the container"""
    ctx.run("echo 'To ssh into the running docker container, execute the following'")
    ctx.run("echo")
    ctx.run("echo 'docker exec -it app1 /bin/bash'")


@task
def db(ctx, config_name="dev", cmd="--help"):
    """Start the backend as a dev server or production ready gunicorn server"""

    ctx.run(
        f"""
        export FLASK_ENV=development &&
        export FLASK_APP="{TASK_DIR}/app:create_app('{config_name}')" &&
        flask db {cmd}
        """,
        pty=True,
        echo=True,
    )
