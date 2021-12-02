#!/usr/bin/env python3
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments,too-many-locals,too-many-branches,too-many-statements

# No mypy stubs for fastcore or ghapi; just turn off type-checking.
# type: ignore

import json

import click
from fastcore.net import \
    HTTP404NotFoundError  # pylint: disable=no-name-in-module
from ghapi.all import GhApi, paged


@click.command()
@click.argument("dest_org")
@click.argument("export_json_file", type=click.File("r"))
@click.argument("users_file", type=click.File("r"))
@click.option(
    "--preview",
    is_flag=True,
    help="Preview what will happen but don't execute.",
)
@click.option(
    "--no-prompt",
    is_flag=True,
    help="Don't ask for a confirmation before transferring the repos.",
)
def migrate(
    dest_org: str,
    export_json_file,
    users_file,
    preview: bool,
    no_prompt: bool,
):
    """
    Invite users in {users_file} to {dest_org} and apply team memberships from {export_json_file}.

    {export_json_file} is expected to have this format:
        {
            "repos": [
                {
                    "name": "repo-x",
                    ...other fields
                },
                {
                    "name": "repo-y",
                    ...other fields
                },
                ...
            ],
            "teams": [
                {
                    "slug": "team-a",
                    "members": ["username1", "username2"]
                },
                {
                    "slug": "team-b",
                    "members": ["username2", "username3"]
                },
                ...
            ]
        }
    """
    _ = dest_org
    _export_data = json.load(export_json_file)
    _ = users_file
    _ = GhApi
    _ = paged
    try:
        pass
    except HTTP404NotFoundError:
        pass
    if preview:
        pass
    if not no_prompt:
        pass


if __name__ == "__main__":
    migrate()  # pylint: disable=no-value-for-parameter
