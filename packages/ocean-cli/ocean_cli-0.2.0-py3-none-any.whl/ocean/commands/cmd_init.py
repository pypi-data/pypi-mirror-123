import click
import os
import requests

from ocean import code
from ocean.main import Environment
from ocean.utils import print, PrintType


@click.command()
@click.option("--url", default="http://ocean-backend-svc:8000", help="pass backend url")
def cli(url):
    ctx = Environment(load=False)

    # make .oceanrc on home-dir and init
    if not ctx.config_path.exists():
        ctx.config_path.parent.mkdir(exist_ok=True)
        ctx.config_path.touch()

    try:
        res = requests.get(url + "/api/healthz")
        if res.status_code != 404:
            raise ValueError()

    except (requests.exceptions.ConnectionError, ValueError):
        print(
            "Server is not responding. Please check `--url` is correct.",
            PrintType.FAILED,
        )
        return

    # save env
    ctx.update_config(code.OCEAN_URL, url)
    ctx.update_config("presets", [])

    print("Setup Success.", PrintType.SUCCESS)
