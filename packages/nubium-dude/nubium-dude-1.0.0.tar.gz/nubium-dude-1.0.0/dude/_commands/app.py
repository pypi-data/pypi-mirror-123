from . import dude_cli
from .._utils import (
    run_command_in_virtual_environment,
    read_file,
    write_file,
    sync_virtual_environment,
    is_nubium_app,
    is_faust_app,
    has_requirements,
    download_file,
)
from pathlib import Path
import click
from dotenv import load_dotenv
from os import environ, remove
from nubium_utils.confluent_utils import KafkaToolbox


@dude_cli.group("app")
def app_group():
    pass


@app_group.command("run")
@click.option("--skip-topic-creation", is_flag=True)
def run(skip_topic_creation):
    if is_nubium_app():
        sync_virtual_environment()
        load_dotenv(Path(f'{environ["DUDE_APP_VENV"]}/.env'))
        if not skip_topic_creation:
            topics = {environ[var]: '' for var in environ if '_TOPIC' in var}
            KafkaToolbox().create_topics(topics, ignore_nubium_topic_cluster_maps=True)
        run_command_in_virtual_environment('python3.8', args=['app.py'])


@app_group.command("sync")
@click.option("--wipe-existing", is_flag=True)
def sync(wipe_existing):
    if is_nubium_app():
        sync_virtual_environment(wipe_existing=wipe_existing)


@app_group.command("unit_test")
def unit_test():
    if is_nubium_app():
        sync_virtual_environment()
        run_command_in_virtual_environment("pytest")


@app_group.command("build_reqs")
@click.option("--image-branch", default='master', type=str)
def build_requirements(image_branch):
    if is_nubium_app() and has_requirements():
        sync_virtual_environment()
        file = f'https://gitlab.corp.redhat.com/mkt-ops-de/mktg-ops-images/-/raw/{image_branch}/confluent-base/requirements.txt'
        if is_faust_app():
            file = f'https://gitlab.corp.redhat.com/mkt-ops-de/mktg-ops-images/-/raw/{image_branch}/streams-base/requirements.txt'
        base_reqs = Path(f'{environ["DUDE_APP_VENV"]}/base_requirements.txt')
        download_file(file, base_reqs, replace_existing=True)

        tmp_reqs = f'./requirements.in.tmp'
        tmp_reqs_data = [line.replace("${DUDE_APP_VENV}", environ["DUDE_APP_VENV"]) for line in read_file('./requirements.in')]
        write_file(tmp_reqs_data, tmp_reqs)

        run_command_in_virtual_environment(
            "pip-compile",
            args=['--output-file=./requirements.txt', tmp_reqs])
        remove(tmp_reqs)
