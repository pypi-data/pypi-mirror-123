#!/usr/bin/env python
import argparse
import random
import time
from typing import Text

from cnside import metadata, errors
from cnside.authenticator import Authenticator, AuthenticatorConfig
from cnside.cli import APIClient, APIClientConfig
from cnside.cli.core import PrintColors, ParsedWrappedCommand, generate_request_document, \
    execute_command
from cnside.storage import StorageHandlerConfig, StorageHandler


class Joker:
    def __init__(self):
        self.colors = PrintColors()

    def ill_let_myself_out(self):
        if not random.randint(0, 1000):
            time.sleep(1)
            self.colors.point_warning("ENCRYPTING ALL YOUR COMPUTER FILES!")
            time.sleep(3)
            self.colors.point_fail("SYKE!!! THE FILE ENCRYPTION MODE IS DISABLED. 😑")
            time.sleep(1)
            self.colors.point("TIP: To enable file encryption mode run 'cnside --enable-encrypt-my-file'")


def interface():
    """
    Provides script interface for end user.

    """
    # todo: build a hierarchical parser for all commands
    parser = argparse.ArgumentParser(usage="cnside [PACKAGE MANAGER COMMAND]\n"
                                           "Command Line Interface Tool for interacting with CNSIDE Service\n"
                                           "Usage example: cnside pip install flask".format(__file__))
    parser.add_argument("manager", help="Package Manager (Supported: pip, npm, nuget, maven, illustria)")
    parser.add_argument("action", help="Action (install, auth)")
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    cli_command = ParsedWrappedCommand(package_manager=args.manager, action=args.action, arguments=args.arguments)
    return cli_command


def request_packages(command: ParsedWrappedCommand, api_client: APIClient, cnside_npm_repo: Text,
                     cnside_pypi_repo: Text, skip_install: bool = False):
    colors = PrintColors()

    request_document = generate_request_document(command)

    # ill_let_myself_out()

    colors.header("Requesting packages from CNSIDE System.")
    if request_document.packages:
        colors.point(f"Packages: {request_document.packages}")
    else:
        colors.point(f"Manifest: {request_document.manifest}")

    approved = api_client.request_packages_from_cnside_system(request_document=request_document)
    if approved:
        colors.point_ok("LIBRARY APPROVED")
        if command.package_manager == metadata.packages.PackageManagers.NPM:
            command.arguments.extend(["--registry", cnside_npm_repo])
        elif command.package_manager == metadata.packages.PackageManagers.PIP:
            command.arguments.extend(["--index-url", cnside_pypi_repo])
        else:
            raise errors.UnsupportedPackageManager()
        if not skip_install:
            execute_command(command=command)
        else:
            colors.point_warning("Skipping Installation (skip_install=True)")
    else:
        colors.point_fail("LIBRARY REJECTED")


def main():
    command = interface()

    # todo: save to config file
    cnside_base_url = "https://cnside.illustria.io"
    cnside_npm_repo = "https://repo.illustria.io/repository/cnside_npm_hosted/"
    cnside_pypi_repo = "https://repo.illustria.io/repository/cnside_pypi_hosted/simple"
    auth_url = "https://illustria.frontegg.com/oauth/authorize"
    token_url = "https://illustria.frontegg.com/oauth/token"

    storage_handler = StorageHandler(StorageHandlerConfig())

    authenticator = Authenticator(
        config=AuthenticatorConfig(auth_url=auth_url, token_url=token_url, storage_handler=storage_handler)
    )

    if command.package_manager == "illustria":
        index = {
            "auth": authenticator.authenticate
        }
        index[command.action]()
    else:
        token = authenticator.token()
        api_client = APIClient(
            config=APIClientConfig(
                base_url=cnside_base_url,
                headers={"Authorization": f"{token.token_type} {token.access_token}"}
            )
        )

        try:
            request_packages(command=command, api_client=api_client,
                             cnside_npm_repo=cnside_npm_repo, cnside_pypi_repo=cnside_pypi_repo)
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
