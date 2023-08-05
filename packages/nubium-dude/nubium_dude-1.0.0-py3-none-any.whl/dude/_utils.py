import os
from pathlib import Path
import pty
import select
import subprocess
from typing import List
from os import environ, remove
from dotenv import load_dotenv
from shutil import copy2, rmtree
import requests
import click
from virtualenvapi.manage import VirtualEnvironment
from virtualenv import cli_run
from nubium_utils._local_env_defaults import local_dotenv_dict


def download_file(url, dest: Path, replace_existing=False):
    # TODO: use wget?
    # import wget
    # wget.download(url, '/Users/scott/Downloads/cat4.jpg')
    dest.parent.mkdir(parents=True, exist_ok=True)
    file = requests.get(url).content
    if dest:
        if replace_existing and dest.is_file():
            remove(dest)
        with open(dest, "wb") as f:
            f.write(file)
    return file


def read_file(file):
    with open(file, 'r') as f:
        file_out = f.readlines()
    return file_out


def write_file(line_list, file):
    with open(file, 'w') as f:
        f.writelines(line_list)


def has_requirements():
    return Path('requirements.in').is_file()


def is_nubium_app():
    # TODO: Turn this into a decorator?
    return Path('app.py').is_file()


def is_faust_app():
    return Path('kiwf_openshift_health_check.py').is_file()


def import_dotenvs():
    if environ.get('DUDE_CONFIG_DOTENV'):
        load_dotenv(environ['DUDE_CONFIG_DOTENV'])
    else:
        load_dotenv(f'{Path(__file__).parent}/config.env')
    environ.update(local_dotenv_dict)

    override = bool(environ.get('DUDE_ALLOW_DOTENV_OVERRIDE'))
    for var in ['DUDE_CREDENTIALS_DOTENV', 'DUDE_NUBIUM_DOTENV', 'DUDE_CUSTOM_DOTENV']:
        if environ.get(var):
            load_dotenv(environ[var], override=override)


def sync_virtual_environment(wipe_existing=False):
    # TODO load virtualenv path from configuration
    venv_path = Path(f'{environ["DUDE_APP_VENV"]}')
    if wipe_existing:
        rmtree(venv_path)
    venv_path.mkdir(parents=True, exist_ok=True)
    # TODO load python version from configuration
    cli_run([str(venv_path), "-p", "python3.8"])
    venv = VirtualEnvironment(str(venv_path), readonly=True)
    if not venv.is_installed("pip-tools"):
        # TODO lock versions of pip-tools and dependencies
        run_command_in_virtual_environment("pip", args=["install", "pip-tools"])
    run_command_in_virtual_environment("pip-sync")
    local_dotenv = Path('configs/local.env')
    venv_dotenv = Path(f'{venv_path}/.env')
    if local_dotenv.is_file() and not venv_dotenv.is_file():
        copy2(local_dotenv, venv_dotenv)


def run_command_in_virtual_environment(
    command: str = '',
    venv_path: Path = None,
    args: List[str] = None
):
    if not venv_path:
        venv_path = Path(f'{environ["DUDE_APP_VENV"]}')
    if not args:
        args = []
    run_command_in_pseudo_tty(command=str(venv_path / "bin" / command), args=args)


def run_command_in_pseudo_tty(
    command: str,
    args: List[str] = None,
    output_handler=lambda data: click.echo(data, nl=False),
    buffer_limit=512,
    buffer_timeout_seconds=0.04,
):
    # In order to get colored output from a command, the process is unfortunately quite involved.
    # Constructing a pseudo terminal interface is necessary to fake most commands into thinking they are in an environment that supports colored output
    if not args:
        args = []

    # It's possible to handle stderr separately by adding p.stderr.fileno() to the rlist in select(), and setting stderr=subproccess.PIPE
    # which would enable directing stderr to click.echo(err=True)
    # probably not worth the additional headache
    master_fd, slave_fd = pty.openpty()
    proc = subprocess.Popen([command] + args, stdin=slave_fd, stdout=slave_fd, stderr=subprocess.STDOUT, close_fds=True)

    def is_proc_still_alive():
        return proc.poll() is not None

    while True:
        ready, _, _ = select.select([master_fd], [], [], buffer_timeout_seconds)
        if ready:
            data = os.read(master_fd, buffer_limit)
            output_handler(data)
        elif is_proc_still_alive():  # select timeout
            assert not select.select([master_fd], [], [], 0)[0]  # detect race condition
            break  # proc exited
    os.close(slave_fd)  # can't do it sooner: it leads to errno.EIO error
    os.close(master_fd)
    proc.wait()
