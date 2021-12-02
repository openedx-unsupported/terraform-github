#!/usr/bin/env python3
# pylint: disable=missing-module-docstring

# no type stubs for ghapi :(
# type: ignore


import json

import click
from ghapi.all import GhApi


@click.command()
@click.argument("export_json_file", type=click.File("r"))
@click.option(
    "--github_token",
    envvar="GITHUB_TOKEN",
    required=True,
)
def json_to_userlist(export_json_file, github_token):
    """
    Given an a JSON GitHub org export, generate an alphabetized list of usernames.

    Reads from {export_json_file}, prints to STDOUT.

    Usernames will be included for all users who:
    * are on a team, and/or
    * have direct access to a repo.
    Otherwise, the user wouldn't be represtented in the JSON export.
    """
    api = GhApi(token=github_token)

    export = json.load(export_json_file)
    usernames_from_teams = set(
        user for team in export["teams"] for user in team["members"]
    )
    usernames_from_repos = set(
        user for repo in export["repos"] for user in repo["user_access"].keys()
    )
    all_usernames = sorted(usernames_from_teams | usernames_from_repos)

    user_dicts = {}
    for username in all_usernames:
        user_dicts[username] = {
            "username": username,
            "user_id": api.users.get_by_username(username)["id"],
        }

    print(json.dumps(user_dicts, indent=4))


if __name__ == "__main__":
    json_to_userlist()  # pylint: disable=no-value-for-parameter
