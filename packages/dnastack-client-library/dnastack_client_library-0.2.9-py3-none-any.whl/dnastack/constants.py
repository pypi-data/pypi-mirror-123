import os

__version__ = "0.2.9"

# This is the public client wallet.publisher.dnastack.com used if the user does not set their own
default_auth = {
    "wallet_uri": "https://wallet.publisher.dnastack.com",
    "redirect_uri": "https://wallet.publisher.dnastack.com/",
    "client_id": "publisher-cli",
    "client_secret": "WpEmHtAiB73pCrhbEyci42sBFcfmWBdj",
}

cli_directory = f"{os.path.expanduser('~')}/.dnastack"
config_file_path = f"{cli_directory}/config.yaml"
downloads_directory = f"{os.getcwd()}"

ACCEPTED_CONFIG_KEYS = [
    "data-connect-url",
    "personal_access_token",
    "email",
    "oauth_token",
    "wallet-url",
    "client-id",
    "client-secret",
    "client-redirect-uri",
    "collections-url",
    "wes-url",
]

auth_scopes = (
    "openid "
    "offline_access "
    "drs-object:write "
    "drs-object:access "
    "dataconnect:info "
    "dataconnect:data "
    "dataconnect:query "
    "wes"
)
