import click

from ocean import code
from ocean.main import pass_env
from ocean.utils import print, PrintType


@click.command()
@pass_env
def cli(ctx):
    ctx.update_config(code.TOKEN, "")
    print("Logout Success.", PrintType.SUCCESS)
