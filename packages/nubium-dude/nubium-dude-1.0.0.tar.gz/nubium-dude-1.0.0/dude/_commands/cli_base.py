import runpy
import sys
import click
from dude._utils import import_dotenvs


@click.group(invoke_without_command=True)
@click.version_option(prog_name="dude")
@click.pass_context
def dude_cli(ctx):
    import_dotenvs()
    if ctx.invoked_subcommand is None:
        print_help()


@dude_cli.command("format")
def auto_format():
    sys.argv[1:] = ["."]
    runpy.run_module("black")


@dude_cli.command()
def lint():
    click.echo("TODO: run linter")


def print_help():
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
