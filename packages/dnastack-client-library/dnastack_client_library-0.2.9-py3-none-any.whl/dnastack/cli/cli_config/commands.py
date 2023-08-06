import click
import yaml
import json

from dnastack.constants import *
from dnastack.cli.utils import *


class ConfigHelp(click.Command):
    def format_help(self, ctx, formatter):
        click.echo("Usage: dnastack config set [OPTIONS] KEY VALUE")
        click.echo("Options:")
        click.echo(" --help  Show this message and exit.")
        click.echo("Accepted Keys: ")
        for key in ACCEPTED_CONFIG_KEYS:
            click.echo(f"\t{key}")


@click.group()
@click.pass_context
def config(ctx: click.Context):
    pass


@config.command(name="list")
@click.pass_context
def config_list(ctx: click.Context):
    click.echo(json.dumps(ctx.obj, indent=4))
    return


@config.command()
@click.pass_context
@click.argument("key")
def get(ctx: click.Context, key: str):
    var_path = key.split(".")
    assert_config(ctx, var_path[0])

    try:
        val = get_config(ctx, var_path)
    except Exception as e:
        click.secho(e, fg="red")
        sys.exit(1)

    output = json.dumps(val, indent=4)

    # we don't want surrounding quotes in our single string outputs so remove them
    if type(val) == str:
        output = output.replace('"', "")

    click.echo(output)
    return


@config.command(name="set")
@click.pass_context
@click.argument("key")
@click.argument("value", required=False, default=None, nargs=1)
def config_set(ctx, key, value):
    key = key.split(".")

    assert_config_key(key[0])

    set_config(ctx, key, value)

    click.echo(json.dumps(ctx.obj, indent=4))
