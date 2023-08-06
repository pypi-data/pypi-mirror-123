import click
from simple_term_menu import TerminalMenu
import os

from ocean import api, code, utils
from ocean.main import pass_env
from ocean.commands import cmd_get, cmd_logs, cmd_delete
from ocean.utils import print, PrintType


@click.group(cls=utils.AliasedGroup)
def cli():
    pass


# Workloads
@cli.command()
@click.argument("name")
@click.option("-p", "--preset", help="run job with preset configuration")
@click.option("--purpose", default="None", help="purpose of job")
@click.option("-i", "--image", help="base docker image")
@click.option("-m", "--machine-type", help="machine-type to run this job")
@click.option("-v", "--volume", help="mounted volume")
@click.option("-r", "--repeat", default=1, help="how many repeat same job")
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="debug mode. follows logs and delete when finished.",
)
@click.argument("command", nargs=-1, type=click.Path())
@pass_env
def job(
    ctx, name, preset, purpose, image, machine_type, volume, repeat, debug, command
):
    if preset:
        presets = utils.dict_to_namespace(ctx.get_presets())
        for p in presets:
            if preset == p.name:
                image = p.image
                machine_type = p.machineType
                volume = p.volume
                break
        else:
            print("Invalid `preset`.", PrintType.FAILED)
            print("Please check allowed preset here:\n\n\tocean get preset\n")
            exit()
    else:
        presets = utils.dict_to_namespace(ctx.get_presets())
        for p in presets:
            if p.default:
                image = p.image
                machine_type = p.machineType
                volume = p.volume
                break

    if purpose == "" or purpose is None:
        print("`purpose` cannot be blank.", PrintType.FAILED)
        exit()

    mid = api.get_id_from_machine_type(ctx, machine_type)
    if mid is None:
        print("Invalid `machine-type`.", PrintType.FAILED)
        print("Please check allowed machine-type here:\n\n\tocean get quota\n")
        exit()

    vid = api.get_volume_id_from_volume_name(ctx, volume)

    data = {
        code.NAME: name,
        code.PURPOSE: purpose,
        code.IMAGE: image,
        code.MACHINETYPEID: mid,
        code.VOLUMENAME: vid,
        code.REPEAT: repeat,
        code.COMMAND: " ".join(command),
    }

    res = api.post(ctx, code.API_JOB, data=data)
    print(f"Job `{name}` Created.", PrintType.SUCCESS)

    if debug:
        # show logs
        cmd_logs._logs(ctx, name, 0)

        # delete job
        cmd_delete._jobs(ctx, name)


@cli.command()
@pass_env
def presets(ctx):
    try:
        name = click.prompt("Preset Name")
        presets = ctx.get_presets()
        while name in map(lambda x: x['name'], presets):
            print(f"Preset `{name}` already exit.\n", PrintType.FAILED)
            name = click.prompt("Preset Name")

        print("MachineType: ")
        machine_types = cmd_get._quota(ctx)
        select_menu = TerminalMenu([machine_types.fstring.format(*x) for x in machine_types.items])
        menu_entry_index = select_menu.show()
        machine_type = machine_types.items[menu_entry_index][0]
        print(f"\033[AMachineType: {machine_type}")

        print("Image: ")
        images = cmd_get._images(ctx)
        select_menu = TerminalMenu([images.fstring.format(*x) for x in images.items])
        menu_entry_index = select_menu.show()
        image = images.items[menu_entry_index][0]
        print(f"\033[AImage: {image}")

        print("Volume: ")
        volumes = cmd_get._volumes(ctx)
        select_menu = TerminalMenu([volumes.fstring.format(*x) for x in volumes.items])
        menu_entry_index = select_menu.show()
        volume = volumes.items[menu_entry_index][0]
        print(f"\033[AVolume: {volume}")

        default = click.confirm("Set to default?")
    except TypeError as e:
        print("Abort!", PrintType.FAILED)
        return

    preset = {
        code.NAME: name,
        code.MACHINETYPE: machine_type,
        code.IMAGE: image,
        code.VOLUME: volume,
        code.DEFAULT: default,
    }

    ctx.add_presets(preset)
    print(f"Preset `{name}` Created.", PrintType.SUCCESS)


def get_idx(message, length):
    id = click.prompt(message, type=int)
    in_range = id in range(length)
    while not in_range:
        print(f"Error: '{id}' is not a valid integer.", PrintType.FAILED)
        id = click.prompt(message, type=int)
        in_range = id in range(length)
    return id
