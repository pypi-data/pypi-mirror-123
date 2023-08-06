import click
from datetime import datetime, timezone
from getpass import getpass

from ocean import api, code, utils
from ocean.main import pass_env
from ocean.utils import print, PrintType


@click.group(cls=utils.AliasedGroup)
def cli():
    pass


# Workloads
@cli.command()
@pass_env
def instances(ctx):
    res = api.get(ctx, "/api/instances/")
    body = utils.dict_to_namespace(res.json())

    fstring = "{:20} {:10} {:15} {:15}"

    print(fstring.format("NAME", "STATUS", "TYPE", "VOLUME"))
    for pods in body.pods:
        print(
            fstring.format(
                pods.name,
                pods.status,
                pods.labels.machineType.name,
                pods.volumes[0].persistentVolumeClaim.claimName,
            )
        )


@cli.command()
@click.option("-d", "--detail", help="Show selected sub tasks detail")
@click.option(
    "-A",
    "--detail-all",
    is_flag=True,
    help="Show all sub tasks detail. `--detail` option will be ignored.",
)
@pass_env
def jobs(ctx, detail, detail_all):
    detail = detail.split(",") if detail else None

    # conditions
    print_detail = detail or detail_all
    print_simple = (detail is None) and (not detail_all)
    filter_job = lambda x: print_simple or detail_all or (x in detail)

    # api call
    res = api.get(ctx, "/api/jobs/")
    body = utils.dict_to_namespace(res.json())

    fstring = "{:15} {:8} {:8} {:8} {:15} {:15} {:40} {:20}"

    print(
        fstring.format(
            "NAME",
            "PENDING",
            "RUNNING",
            "FINISHED",
            "TYPE",
            "VOLUME",
            "IMAGE",
            "COMMAND",
        )
    )
    for jobInfo in body.jobsInfos:
        if not filter_job(jobInfo.name):
            continue

        pending, running, succeeded, failed = 0, 0, 0, 0
        details = []
        for job in jobInfo.jobs:
            status = job.jobPodInfos[0].status
            if status == "Pending":
                pending += 1
            elif status == "Running":
                running += 1
            elif status == "Succeeded":
                succeeded += 1
            elif status == "Failed":
                failed += 1

            if print_detail:
                start_time = utils.convert_time(job.startTime)
                complete_time = utils.convert_time(job.completionTime)
                delta = 0
                if status == "Running":
                    delta = (
                        datetime.now(timezone.utc).replace(microsecond=0) - start_time
                    )
                elif status == "Succeeded":
                    delta = complete_time - start_time

                start_time = utils.date_format(start_time)
                complete_time = utils.date_format(complete_time)

                details.append(
                    f"{job.name:20} {job.jobPodInfos[0].status:10} {start_time} ~ {complete_time} ({delta})"
                )

        print(
            fstring.format(
                jobInfo.name,
                str(pending),
                str(running),
                f"{succeeded}/{failed}",
                jobInfo.labels.machineType.name,
                jobInfo.volumes[0].persistentVolumeClaim.claimName,
                jobInfo.image,
                jobInfo.command,
            )
        )
        if print_detail:
            print("\n".join(details))
            print()


@cli.command()
@pass_env
def volumes(ctx):
    content = _volumes(ctx)

    print(content.fstring.format(*content.header))
    for item in content.items:
        print(content.fstring.format(*item))


def _volumes(ctx):
    res = api.get(ctx, "/api/volumes/")
    body = utils.dict_to_namespace(res.json())

    content = utils.dict_to_namespace(
        {
            "fstring": "{:20} {:10} {:10}",
            "header": ["NAME", "STATUS", "CAPACITY"],
            "items": [],
        }
    )

    for vol in body.volumes:
        content.items.append([vol.name, vol.status, vol.capacity])

    return content


# Resources
@cli.command()
@pass_env
def images(ctx):
    content = _images(ctx)

    print(content.fstring.format(*content.header))
    for item in content.items:
        print(content.fstring.format(*item))


def _images(ctx, show_id=False):
    res = api.get(ctx, "/api/images/")
    body = utils.dict_to_namespace(res.json())

    content = utils.dict_to_namespace(
        {"fstring": "{:6} {:60} {}", "header": ["TYPE", "IMAGE", "LABLES"], "items": []}
    )

    for img in body.public + body.user:
        content.items.append([img.imageType, img.imageName, ",".join(img.imageLabels)])
    # for img in body.user:
    #     content.items.append([img.imageName])
    return content


@cli.command()
@pass_env
def quota(ctx):
    content = _quota(ctx)

    print(content.fstring.format(*content.header))
    for item in content.items:
        print(content.fstring.format(*item))


def _quota(ctx):
    res = api.get(ctx, "/api/users/resources")

    body = utils.dict_to_namespace(res.json())

    content = utils.dict_to_namespace(
        {
            "fstring": "{:20} {:10} {:100}",
            "header": ["NAME", "QUOTA", "SPEC"],
            "items": [],
        }
    )

    for mt in body.machineTypes:
        content.items.append(
            [
                mt.name,
                f"{mt.quotaUsedIn}/{mt.quota}",
                f"CPU {mt.cpus:2}, MEM {mt.memory:3} Gi, GPU {mt.gpus:1} x {mt.gpuType}",
            ]
        )

    return content


@cli.command()
@pass_env
def machine_types(ctx):
    content = _machine_types(ctx)

    print(content.fstring.format(*content.header))
    for item in content.items:
        print(content.fstring.format(*item))


def _machine_types(ctx):
    res = api.get(ctx, "/api/machinetypes/")

    body = utils.dict_to_namespace(res.json())

    content = utils.dict_to_namespace(
        {"fstring": "{:20} {:100}", "header": ["NAME", "QUOTA", "SPEC"], "items": []}
    )

    for mt in body:
        content.items.append(
            [
                mt.name,
                f"CPU {mt.cpus:4}, MEM {mt.memory:5} Gi, GPU {mt.gpus:1} x {mt.gpuType}",
            ]
        )
    return content


# CLI ENV
@cli.command()
@pass_env
def presets(ctx):
    _presets(ctx)


def _presets(ctx, show_id=False):
    fstring = "{:20} {:20} {:20} {:40}"
    fstring = "{id:5} " + fstring if show_id else fstring

    print(fstring.format("NAME", "TYPE", "VOLUME", "IMAGE", id="ID"))
    for preset in utils.dict_to_namespace(ctx.get_presets()):
        default_txt = " (default)" if preset.default else ""
        print(
            fstring.format(
                preset.name + default_txt,
                preset.machineType,
                preset.volume,
                preset.image,
            )
        )
