import sys
from typing import Any, Union

import click
import yaml
from dnastack.constants import config_file_path, ACCEPTED_CONFIG_KEYS


# Getters
def get_config(
    ctx: click.Context,
    var_path: Union[list, str],
    val_type: Any = None,
    do_assert: bool = False,
):
    if type(var_path) == str:
        var_path = [var_path]
    # assert that the config is there
    # we only do this assertion for the root level configs as of currently
    if do_assert:
        assert_config(ctx, var_path[0], val_type=val_type)

    try:
        obj = ctx.obj
        for key in var_path[:-1]:
            obj = obj[key]
    except KeyError as k:
        raise k
    except Exception as e:
        raise Exception(f"Could not get the config variable at {'.'.join(var_path)}")

    # for the last object we don't error if it's not there, just return None
    return obj.get(var_path[-1])


# Setters


def set_config(ctx: click.Context, var_path: Union[list, str], value: Any):
    if type(var_path) == str:
        var_path = [var_path]
    assert len(var_path) >= 1
    set_config_obj(ctx.obj, var_path, value)
    with open(config_file_path, "w") as config_file:
        yaml.dump(ctx.obj, config_file)


def set_config_obj(obj: dict, var_path: list, value: Any):

    var_name = var_path[0]
    if var_name not in obj.keys():
        obj[var_name] = None

    if len(var_path) == 1:
        obj[var_name] = value
    else:
        if obj[var_name] is not None:
            assert type(obj[var_name]) == dict
            set_config_obj(obj[var_name], var_path[1:], value)
        else:
            obj[var_name] = {}
            set_config_obj(obj[var_name], var_path[1:], value)


# Checks


def is_config_key(var_name: str):
    return var_name in ACCEPTED_CONFIG_KEYS


def has_config(ctx: click.Context, var_name: str):
    return var_name in ctx.obj.keys() and ctx.obj[var_name]


def has_type(ctx: click.Context, var_name: str, val_type: type):
    return type(ctx.obj[var_name]) == val_type if val_type is not None else True


# Assertions


def assert_config(ctx: click.Context, var_name: str, val_type: type = None):
    assert_config_key(var_name)
    if not has_config(ctx, var_name):
        click.secho(
            f"The {var_name} configuration variable is not set. Run dnastack config set {var_name} [{var_name.upper()}] to configure it",
            fg="red",
        )
        sys.exit(1)
    elif not has_type(ctx, var_name, val_type):
        click.secho(
            f"The {var_name} configuration variable is not a {val_type.__name__} type. Run dnastack config set {var_name} [{var_name.upper()}] to reconfigure it",
            fg="red",
        )
        sys.exit(1)


def assert_config_key(key: str):
    if not is_config_key(key):
        click.secho(f"{key} is not an accepted configuration key.", fg="red")
        click.secho(f"Accepted configuration keys:", fg="red")
        for key in ACCEPTED_CONFIG_KEYS:
            click.secho(f"\t{key}", fg="red")
        sys.exit(1)


def get_auth_params(ctx: click.Context, do_assert: bool = False):
    auth_params = {
        "wallet_uri": get_config(ctx=ctx, var_path="wallet-url", do_assert=do_assert),
        "redirect_uri": get_config(
            ctx=ctx, var_path="client-redirect-uri", do_assert=do_assert
        ),
        "client_id": get_config(ctx=ctx, var_path="client-id", do_assert=do_assert),
        "client_secret": get_config(
            ctx=ctx, var_path="client-secret", do_assert=do_assert
        ),
    }

    return auth_params
