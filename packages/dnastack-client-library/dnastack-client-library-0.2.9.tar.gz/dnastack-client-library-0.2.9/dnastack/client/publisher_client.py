from . import *
from dnastack import constants
from pandas import DataFrame
from getpass import getpass
from typing import Any, Optional
import json


class PublisherClient:
    def __init__(
        self,
        email=None,
        personal_access_token=None,
        dataconnect_url=None,
        collections_url=None,
        wes_url=None,
        auth_params=default_auth,
    ):
        self.dataconnect_url = dataconnect_url
        self.collections_url = collections_url
        self.wes_url = wes_url

        self.dataconnect = self.dataconnect(self)
        self.collections = self.collections(self)
        self.wes = self.wes(self)
        self.auth = self.auth(auth_params, personal_access_token, email, self)

    class dataconnect:
        def __init__(self, parent):
            self.parent = parent

        def query(self, q, download=False):
            return json.loads(
                dataconnect_client.query(
                    self.parent.dataconnect_url,
                    q,
                    download,
                    oauth_token=self.parent.auth.oauth_token,
                )
            )

        def list_tables(self):
            return json.loads(
                dataconnect_client.list_tables(
                    self.parent.dataconnect_url, self.parent.auth.oauth_token
                )
            )

        def get_table(self, table_name):
            return json.loads(
                dataconnect_client.get_table(
                    self.parent.dataconnect_url,
                    table_name,
                    self.parent.auth.oauth_token,
                )
            )

    class collections:
        def __init__(self, parent):
            self.parent = parent

        def list(self):
            return collections_client.list_collections(self.parent.collections_url)

        def list_tables(self, collection_name):
            return collections_client.list_tables(
                self.parent.collections_url, collection_name
            )

        def query(self, collection_name, query):
            return json.loads(
                collections_client.query(
                    self.parent.collections_url, collection_name, query
                )
            )

    class wes:
        def __init__(self, parent):
            self.parent = parent

        def info(self):
            return get_service_info(
                wes_url=self.parent.wes_url,
                oauth_token=self.parent.auth.oauth_token,
                auth_params=self.parent.auth.auth_params,
            )

        def execute(
            self,
            workflow_url,
            attachment_files: Any = None,
            input_params_file: Any = None,
            engine_param: Any = None,
            engine_params_file: Any = None,
            tag: Any = None,
            tags_file: Any = None,
        ):
            return submit_workflow(
                wes_url=self.parent.wes_url,
                workflow_url=workflow_url,
                oauth_token=self.parent.auth.oauth_token,
                auth_params=self.parent.auth.auth_params,
                attachment_files=attachment_files,
                input_params_file=input_params_file,
                engine_param=engine_param,
                engine_params_file=engine_params_file,
                tag=tag,
                tags_file=tags_file,
            )

        def list(self):
            return get_list_of_workflows_executed(
                wes_url=self.parent.wes_url,
                oauth_token=self.parent.auth.oauth_token,
                auth_params=self.parent.auth.auth_params,
            )

        def get(self, run_id: str, status_only: bool = False):
            return get_run_details(
                wes_url=self.parent.wes_url,
                run_id=run_id,
                oauth_token=self.parent.auth.oauth_token,
                auth_params=self.parent.auth.auth_params,
                status_only=status_only,
            )

        def cancel(self, run_id: str):
            return cancel_run(
                wes_url=self.parent.wes_url,
                run_id=run_id,
                oauth_token=self.parent.auth.oauth_token,
                auth_params=self.parent.auth.auth_params,
            )

        def run_logs(
            self,
            run_id: str,
            stderr: bool = False,
            stdout: bool = False,
            url: Any = None,
            task: Any = None,
            index: int = 0,
        ):
            return get_run_logs(
                wes_url=self.parent.wes_url,
                run_id=run_id,
                oauth_token=self.parent.auth.oauth_token,
                auth_params=self.parent.auth.auth_params,
                stderr=stderr,
                stdout=stdout,
                url=url,
                task=task,
                index=index,
            )

    class auth:
        def __init__(
            self,
            auth_params=default_auth,
            personal_access_token=None,
            email=None,
            parent=None,
        ):
            self.auth_params = auth_params
            self.oauth_token = {}
            self.personal_access_token = personal_access_token
            self.email = email
            self.parent = parent

        def login(self, drs_server=None):
            audience = [
                get_audience_from_url(url)
                for url in [
                    drs_server,
                    self.parent.collections_url,
                    self.parent.dataconnect_url,
                    self.parent.wes_url,
                ]
                if url
            ]

            self.oauth_token = login_with_personal_access_token(
                audience=audience,
                email=self.email,
                personal_access_token=self.personal_access_token,
                auth_params=self.auth_params,
            )

        def set_refresh_token(self, token: str):
            self.oauth_token["refresh_token"] = token

        def refresh_token(self):
            if not self.oauth_token or "refresh_token" not in self.oauth_token.keys():
                raise Exception("There is no refresh token configured.")

            self.oauth_token = login_refresh_token(
                token=self.oauth_token, auth_params=self.auth_params
            )

    def load(self, urls, output_dir=downloads_directory):
        download_content = []
        download_files(
            urls=urls,
            output_dir=output_dir,
            oauth_token=self.auth.oauth_token,
            quiet=True,
            out=download_content,
        )
        return download_content

    def download(self, urls, output_dir=downloads_directory):
        return download_files(
            urls=urls,
            output_dir=output_dir,
            oauth_token=self.auth.oauth_token,
            quiet=True,
        )
