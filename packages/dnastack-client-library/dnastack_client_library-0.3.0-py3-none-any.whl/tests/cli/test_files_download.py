import unittest
from click.testing import CliRunner
import pathlib
from dnastack import __main__ as dnastack_cli
import glob

from .utils import set_cli_config
from .. import *


class TestCliFilesCommand(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.data_connect_url = TEST_DATA_CONNECT_URI

        set_cli_config(self.runner, "data_connect.url", self.data_connect_url)

    def test_drs_download(self):
        result = self.runner.invoke(
            dnastack_cli.dnastack,
            [
                "files",
                "download",
                TEST_DRS_URLS[0],
                "-o",
                "out",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(
            pathlib.Path(f"{os.getcwd()}/out/{TEST_DRS_FILENAMES[0]}").exists()
        )

        # clean up ./out directory
        pathlib.Path(f"{os.getcwd()}/out/{TEST_DRS_FILENAMES[0]}").unlink(
            missing_ok=True
        )
        pathlib.Path(f"{os.getcwd()}/out").rmdir()

    def test_multiple_drs_download(self):
        result = self.runner.invoke(
            dnastack_cli.dnastack,
            ["files", "download"]
            + TEST_DRS_URLS
            + [
                "-o",
                "out",
            ],
        )

        self.assertEqual(result.exit_code, 0)

        for drs_file in TEST_DRS_FILENAMES:
            self.assertTrue(pathlib.Path(f"{os.getcwd()}/out/{drs_file}").exists())

        # clean up ./out directory
        for drs_file in TEST_DRS_FILENAMES:
            pathlib.Path(f"{os.getcwd()}/out/{drs_file}").unlink(missing_ok=True)

        pathlib.Path(f"{os.getcwd()}/out").rmdir()

    def test_input_file_flag_drs_download(self):
        with open("download_input_file.txt", "w") as input_file:
            # for some reason writelines doesn't add newlines so add them ourself
            input_file.writelines([f"{drs_url}\n" for drs_url in TEST_DRS_URLS])
            input_file.close()

        result = self.runner.invoke(
            dnastack_cli.dnastack,
            [
                "files",
                "download",
                "-i",
                pathlib.Path("./download_input_file.txt"),
                "-o",
                "out",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        for drs_file in TEST_DRS_FILENAMES:
            self.assertTrue(pathlib.Path(f"{os.getcwd()}/out/{drs_file}").exists())

        # clean up ./out directory
        pathlib.Path(f"{os.getcwd()}/download_input_file.txt").unlink(missing_ok=True)
        for drs_file in TEST_DRS_FILENAMES:
            pathlib.Path(f"{os.getcwd()}/out/{drs_file}").unlink(missing_ok=True)
        pathlib.Path(f"{os.getcwd()}/out").rmdir()

    def test_drs_download_from_broken_url(self):
        result = self.runner.invoke(
            dnastack_cli.dnastack,
            [
                "files",
                "download",
                "drs://drs.international.covidcloud.ca/072f2fb6-8240-4b1e-BROKEN-b736-7868f559c795",
                "-o",
                "out",
            ],
        )
        self.assertIn(
            "Could not get drs object id from url drs://drs.international.covidcloud.ca/072f2fb6-8240-4b1e-BROKEN-b736-7868f559c795",
            result.output,
        )
