import click
from sentry_sdk import set_user

from ocean import api, code
from ocean.main import pass_env
from ocean.utils import print, PrintType


@click.command()
@pass_env
def cli(ctx):
    email = click.prompt("Email")
    password = click.prompt("Password", hide_input=True)

    res = api.post(ctx, code.API_SIGNIN, {code.EMAIL: email, code.PASSWORD: password})

    if res.status_code == 200:
        body = res.json()
        ctx.update_config(code.TOKEN, body.get(code.TOKEN))
        ctx.update_config("username", body.get("user").get("email").split("@")[0])
        set_user({"email": email})
        print("Login Success.", PrintType.SUCCESS)
    else:
        print("Login Failed.", PrintType.Failed)
