#!/usr/bin/env python3
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments,too-many-locals,too-many-branches,too-many-statements

# No mypy stubs for fastcore or ghapi; just turn off type-checking.
# type: ignore

import json
import sys
import time
from collections import defaultdict
from typing import Dict, Set

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
@click.option(
    "--github_token",
    envvar="GITHUB_TOKEN",
    required=True,
)
def migrate(
    dest_org: str,
    export_json_file,
    users_file,
    preview: bool,
    no_prompt: bool,
    github_token: str,
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

    if preview:
        click.secho("In Preview Mode: No changes will be made!", italic=True)
    api = GhApi(token=github_token)

    export_data = json.load(export_json_file)

    all_users = {user_line.trim() for user_line in users_file.readlines()}

    # Load a mapping from team slugs to team ids.
    # Includes teams we're not trying to migrate.
    team_slugs_to_ids = {}
    for page in paged(api.teams.list, org=dest_org, per_page=100):
        for team in page:
            team_slugs_to_ids[team["slug"]] = team["id"]

    # Build a mapping from usernames to team slugs.
    user_teams: Dict[str, Set[int]] = defaultdict(set)
    for team in export_data["teams"]:
        for username in team["members"]:
            user_teams[username].add(team_slugs_to_ids[team["slug"]])

    users_with_pending_invitations: Set[str] = set()
    for page in paged(api.orgs.list_pending_invitations, org=dest_org, per_page=100):
        for user in page:
            users_with_pending_invitations.add(user["login"])

    users_already_in_org: Set[str] = set()
    for page in paged(api.orgs.list_members, org=dest_org, per_page=100):
        for user in page:
            users_already_in_org.add(user["login"])

    users_to_not_invite = users_already_in_org | users_with_pending_invitations

    users_to_invite = all_users - users_to_not_invite

    click.echo(f"Will invite {len(users_to_invite)} to org {dest_org}:")
    click.echo(f"  " + "\n  ".join(users_to_invite))

    if not no_prompt:
        click.echo()
        click.confirm("Proceed?", abort=True)

    for index, username in enumerate(users_to_invite):

        click.echo(f"({index}/{len(users_to_invite)})")

        user_id: int = api.users.get_by_username(username)["id"]

        if preview:
            continue

        # TODO: Wrapp this in a loop for retry purposes.
        try:
            api.orgs.create_invitation(
                org=dest_org,
                invitee_id=user_id,
                team_ids=user_teams[username],
            )
        # Might have hit a secondary rate limit
        # https://docs.github.com/en/rest/overview/resources-in-the-rest-api#secondary-rate-limits
        except HTTP403ForbiddenError as e:
            # Handle the error and retry based on retry header.
            retry_after = e.headers["Retry-After"]
            time.sleep(retry_after + 1)

    _ = dest_org
    _ = GhApi
    _ = paged
    try:
        pass
    except HTTP404NotFoundError:
        pass
    if preview:
        pass


if __name__ == "__main__":
    migrate()  # pylint: disable=no-value-for-parameter
