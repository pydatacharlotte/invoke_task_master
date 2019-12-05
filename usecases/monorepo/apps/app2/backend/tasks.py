""" Utility tasks associated with the current application. """

# Many of these tasks need the app context, and importing app can cause circular
# dependancy issues.
#
# pylint: disable=import-outside-toplevel

import os
import subprocess

from atdcoe_invoke import (clean, cron_deploy, deploy, docker_build,
                           docker_push, docker_run, get_app_dir,
                           init_atdcoe_tasks, install, run, seed, test)
from invoke import task

init_atdcoe_tasks("app2", "app2")


@task
def populate_caches(
    ctx,
    sku_ruleset_name="default",
    style_ruleset_name="default",
    run_from_container=False,
):
    """ Run both of the cache loading scripts. """
    populate_sku_cache(ctx, sku_ruleset_name, run_from_container)
    populate_style_cache(ctx, sku_ruleset_name, style_ruleset_name, run_from_container)


@task
def populate_sku_cache(ctx, sku_ruleset_name="default", run_from_container=False):
    """ Run the cache ETL jobs. """

    if run_from_container:
        run_from_path = "/app"

        subprocess.Popen(
            [
                "/app/cloud_sql_proxy",
                "-instances=a",
                f"-credential_file={run_from_path}/secrets/a.json",
            ]
        )
    else:
        run_from_path = os.path.join(get_app_dir(), "backend")

    with ctx.cd(run_from_path):
        os.chdir(run_from_path)

        from app import create_app
        from app.utils import populate_sku_cache as pop_sku_cache

        print("Creating application.")
        app = create_app("prod")

        with app.app_context():
            print("Populating sku to sku cache.")
            pop_sku_cache(sku_ruleset_name)


@task
def populate_style_cache(
    ctx,
    sku_ruleset_name="default",
    style_ruleset_name="default",
    run_from_container=False,
):
    """ Run the cache ETL jobs. """

    if run_from_container:
        run_from_path = "/app"

        subprocess.Popen(
            [
                "/app/cloud_sql_proxy",
                "-instances=a",
                f"-credential_file={run_from_path}/secrets/a.json",
            ]
        )
    else:
        run_from_path = os.path.join(get_app_dir(), "backend")

    with ctx.cd(run_from_path):
        os.chdir(run_from_path)

        from app import create_app
        from app.utils import populate_style_cache as pop_style_cache

        print("Creating application.")
        app = create_app("prod")

        with app.app_context():
            print("Populating style to style cache.")
            pop_style_cache(sku_ruleset_name, style_ruleset_name)


@task
def import_prices(ctx, run_from_container=False):
    """ Load retail prices from BigQuery. """

    if run_from_container:
        run_from_path = "/app"

        subprocess.Popen(
            [
                "/app/cloud_sql_proxy",
                "-instances=a",
                f"-credential_file={run_from_path}/secrets/a.json",
            ]
        )
    else:
        run_from_path = os.path.join(get_app_dir(), "backend")

    with ctx.cd(run_from_path):
        os.chdir(run_from_path)

        from app import create_app
        from app.utils import import_retail_prices

        app = create_app("prod")

        with app.app_context():
            import_retail_prices()


@task
def populate_style_master(ctx, run_from_container=False):
    """ Populate the style master table from the product master table. """

    if run_from_container:
        run_from_path = "/app"

        subprocess.Popen(
            [
                "/app/cloud_sql_proxy",
                "-instances=a",
                f"-credential_file={run_from_path}/secrets/a.json",
            ]
        )
    else:
        run_from_path = os.path.join(get_app_dir(), "backend")

    with ctx.cd(run_from_path):
        os.chdir(run_from_path)

        from app import create_app
        from app.utils import populate_styles_table

        app = create_app("prod")

        with app.app_context():
            populate_styles_table()
