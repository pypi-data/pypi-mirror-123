import click

from ocean import api, code, utils
from ocean.main import pass_env
from ocean.commands import cmd_get
from ocean.utils import print, PrintType

from sentry_sdk import capture_exception


@click.group(cls=utils.AliasedGroup)
def cli():
    pass


# Workloads
@cli.command()
@click.argument("job-name")
@pass_env
def jobs(ctx, job_name):
    for job in job_name.split(","):
        _jobs(ctx, job)


def _jobs(ctx, job_name):
    # get jobs
    job_ids = []

    res = api.get(ctx, "/api/jobs/")
    body = utils.dict_to_namespace(res.json())
    for jobInfo in body.jobsInfos:
        if jobInfo.name == job_name:
            job_ids = list(map(lambda x: f"{x.uid}", jobInfo.jobs))
            break
    else:
        print(f"Job `{job_name}` not found.", PrintType.FAILED)
        return
    res = api.delete(ctx, "/api/jobs/", data={"jobUids": job_ids})
    print(f"Job `{job_name}` Deleted.", PrintType.SUCCESS)


# CLI ENV
@cli.command()
@click.argument("name")
@pass_env
def presets(ctx, name):
    _presets(ctx, name)
    print(f"Preset `{name}` Deleted.", PrintType.SUCCESS)


def _presets(ctx, name):
    ctx.delete_presets(name)
