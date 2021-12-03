#!/usr/bin/env python3
# pylint: disable=missing-module-docstring

import json

import click


@click.command()
@click.argument("export_json_file", type=click.File("r"))
def json_to_userlist(export_json_file):
    """
    Given an a JSON GitHub org export, generate an alphabetized list of usernames.

    Reads from {export_json_file}, prints to STDOUT.

    Usernames will be included for all users who:
    * are on a team, and/or
    * have direct access to a repo.
    Otherwise, the user wouldn't be represtented in the JSON export.
    """
    export = json.load(export_json_file)
    users_on_teams = set(user for team in export["teams"] for user in team["members"])
    users_in_repos = set(
        user for repo in export["repos"] for user in repo["user_access"].keys()
    )
    print(*sorted(users_on_teams | users_in_repos), sep="\n")


if __name__ == "__main__":
    json_to_userlist()  # pylint: disable=no-value-for-parameter
