import click
import time
import urllib3
import json
import sys

from ocean import api, code, utils
from ocean.main import pass_env
from ocean.utils import print, PrintType

from kubernetes import client, watch, config
from kubernetes.client.rest import ApiException

from sentry_sdk import capture_exception


@click.command()
@click.argument("job-name")
@click.option("-id", default=0, help="Task ID of job.")
@pass_env
def cli(ctx, job_name, id):
    _logs(ctx, job_name, id)


def _logs(ctx, job_name, id):
    # backend api로 job 리스트 가져오기
    res = api.get(ctx, f"/api/jobs")
    body = utils.dict_to_namespace(res.json())
    try:
        for job in body.jobsInfos:
            if job.name == job_name:
                for task in job.jobs:
                    if task.name == job.name + '-' + str(id):
                        print(task.name)
                        _print_logs(ctx, f'{job.labels.user}-{task.name}')
                        break
                else:
                    raise ValueError()
                break
        else:
            raise ValueError()

    except ValueError:
        print("Invalid Job Name. _logs", PrintType.FAILED)


def _get_kube_config():
    config = client.Configuration()

    config.api_key['authorization'] = open('/var/run/secrets/kubernetes.io/serviceaccount/token').read()
    config.api_key_prefix['authorization'] = 'Bearer'
    config.host = 'https://kubernetes.default'
    config.ssl_ca_cert = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
    config.verify_ssl=True

    return config


def _print_logs(ctx, job_name):
    config = _get_kube_config()

    core_api = client.CoreV1Api(client.ApiClient(config))

    label_selector = f"job-name={job_name}"
    response = core_api.list_namespaced_pod(
        namespace="ocean", label_selector=label_selector
    )

    if len(response.items) == 1:
        pod_name = response.items[0].metadata.name
        start = time.time()
        since_seconds = None
        finish = False

        # pending check
        while response.items[0].status.phase == 'Pending':
            response = core_api.list_namespaced_pod(
                namespace="ocean", label_selector=label_selector
            )
            since_seconds = int(time.time() - start + 0.6)
            print(
                f"\033[1GJob is Pending{'.' * ((since_seconds % 5)):4} {since_seconds:3}s",
                PrintType.WORNING,
                nl=False,
            )
            time.sleep(1)
        # sys.stdout.write(
        print("\033[2K\033[1G", nl=False)  # erase and go to beginning of line
        
        while not finish:
            finish = True
            try:
                r = core_api.read_namespaced_pod_log(
                    name=pod_name,
                    namespace="ocean",
                    follow=True,
                    _preload_content=False,
                    _request_timeout=1,
                    since_seconds=since_seconds,
                )
                for log in r:
                    print(log.decode(), nl=False)
                    start = time.time()
                    since_seconds = None
            except urllib3.exceptions.ReadTimeoutError:
                finish = False
                since_seconds = int(time.time() - start + 0.6)
                print(
                    f"Loading{'.' * ((since_seconds % 5)):4} {since_seconds:3}s",
                    PrintType.WORNING,
                    nl=False,
                )
                print("\033[2K\033[1G", nl=False)  # erase and go to beginning of line

            except ApiException as e:
                finish = False
                body = json.loads(e.body)
                print(body["message"], PrintType.FAILED)
                print("\033[2K\033[1G", nl=False)  # erase and go to beginning of line

            except KeyboardInterrupt:
                break

        print("Job Finished.", PrintType.SUCCESS)
    else:
        print("Invalid Job Name.", PrintType.FAILED)
