import sys

import click
from dnastack.client.auth_client import login_device_code, login_refresh_token
from dnastack.client import *
from ..utils import assert_config, get_config, set_config, has_config
import dnastack.constants
import datetime as dt
from urllib.parse import *


def get_oauth_token(ctx):
    if has_config(ctx, "oauth_token"):
        return get_config(ctx, var_path="oauth_token")


def get_auth_params(ctx):
    return {
        "wallet_uri": get_config(ctx, var_path="wallet-url")
        or default_auth["wallet_uri"],
        "redirect_uri": (
            get_config(ctx, var_path="client-redirect-uri")
            or default_auth["redirect_uri"]
        ),
        "client_id": (
            get_config(ctx, var_path="client-id") or default_auth["client_id"]
        ),
        "client_secret": (
            get_config(ctx, var_path="client-secret") or default_auth["client_secret"]
        ),
    }


@click.group()
def auth():
    pass


@auth.command("login")
@click.option("--no-browser", is_flag=True, default=False)
@click.pass_context
def cli_login(ctx, no_browser):
    auth_params = get_auth_params(ctx)

    data_connect_url = get_config(ctx, "data-connect-url")
    collections_url = get_config(ctx, "collections-url")
    wes_url = get_config(ctx, var_path="wes-url")

    if not (data_connect_url or collections_url or wes_url):
        click.secho(
            (
                f"No API urls are configured. "
                f"Configure dnastack with 'dnastack config set (data-connect-url|collections-url|wes-url) URL'"
            ),
            fg="red",
        )
        sys.exit(1)

    audience = [
        get_audience_from_url(url)
        for url in [data_connect_url, collections_url, wes_url]
        if url
    ]

    try:
        access_token = login_device_code(
            audience, auth_params, open_browser=(not no_browser)
        )
    except Exception as e:
        click.secho(f"There was an error generating an access token: {e}", fg="red")
        sys.exit(1)

    set_config(ctx, var_path=["oauth_token"], value=access_token)


@auth.command("refresh")
@click.pass_context
def cli_refresh(ctx):
    auth_params = get_auth_params(ctx)
    try:
        token = get_oauth_token(ctx)
        if not token or not token["refresh_token"] or len(token["refresh_token"]) == 0:
            click.secho("The refresh token does not exist", fg="red")
            sys.exit(1)
        token = login_refresh_token(token, auth_params)
        set_config(ctx, var_path=["oauth_token"], value=token)
    except Exception as e:
        click.secho(f"There was an error refreshing the access token: {e}", fg="red")
        click.secho(f"Please log in again using 'dnastack auth login'", fg="red")
        sys.exit(1)
