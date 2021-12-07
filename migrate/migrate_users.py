#!/usr/bin/env python3
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments,too-many-locals,too-many-branches,too-many-statements

# No mypy stubs for fastcore or ghapi; just turn off type-checking.
# type: ignore

import json
import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Set

import click
from fastcore.net import \
    HTTP403ForbiddenError  # pylint: disable=no-name-in-module
from ghapi.all import GhApi, paged


@click.command()
@click.argument("dest_org")
@click.argument("users_file", type=click.File("r"))
@click.argument("org_export_files", nargs=-1, type=click.File("r"))
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
    org_export_files,
    users_file,
    preview: bool,
    no_prompt: bool,
    github_token: str,
):
    """
    Invite users in {users_file} to {dest_org} and apply team memberships from {org_export_files}.

    {org_export_files} are expected to have this format:
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

    # Load a mapping from team slugs to team ids.
    # Includes teams we're not trying to migrate.
    team_slugs_to_ids = {}
    for page in paged(api.teams.list, org=dest_org, per_page=100):
        for team in page:
            team_slugs_to_ids[team["slug"]] = team["id"]

    # Load team memberships and list of usernames to migrate.
    user_to_teams: Dict[str, Set[Team]] = extract_merged_team_memberships(
        org_export_files,
        team_slugs_to_ids,
    )

    requested_users = set(extract_user_names(users_file))
    # Of the requested users, figure out which ones we shouldn't invite
    # (because they're members or have a pending invite).
    users_pending_invitation: Set[str] = set()
    for page in paged(api.orgs.list_pending_invitations, org=dest_org, per_page=100):
        for user in page:
            users_pending_invitation.add(user["login"])
    users_in_org: Set[str] = set()
    for page in paged(api.orgs.list_members, org=dest_org, per_page=100):
        for user in page:
            users_in_org.add(user["login"])
    requested_users_already_in_org = requested_users & users_in_org
    requested_users_pending_invitation = requested_users & users_pending_invitation
    requested_users_not_to_invite = (
        requested_users_already_in_org | requested_users_pending_invitation
    )
    users_to_invite = requested_users - requested_users_not_to_invite

    click.echo(
        f"{len(requested_users_already_in_org)} users from list are already "
        f"{dest_org} org members."
    )
    click.echo("  " + "\n  ".join(requested_users_already_in_org))

    click.echo(
        f"{len(requested_users_pending_invitation)} users from list have pending "
        f"{dest_org} org invitations."
    )
    click.echo("  " + "\n  ".join(requested_users_pending_invitation))
    click.echo()

    click.secho(
        f"Will invite {len(users_to_invite)} user(s) to org {dest_org}:", bold=True
    )
    click.echo("  " + "\n  ".join(users_to_invite))

    click.secho(
        f"Will update {len(requested_users_already_in_org)} user(s) "
        f"that are already in org {dest_org}:",
        bold=True,
    )
    click.echo("  " + "\n  ".join(requested_users_already_in_org))

    show_prompt = True
    if preview:
        show_prompt = False
    if no_prompt:
        show_prompt = False
    if show_prompt:
        click.echo()
        click.confirm("Proceed?", abort=True)
        click.echo()

    for index, username in enumerate(users_to_invite):
        team_ids = [team.team_id for team in user_to_teams[username]]

        user_id: int = api.users.get_by_username(username)["id"]
        click.echo(
            f"({index:03d}/{len(users_to_invite)}) inviting user {username}; {user_id=}, "
            f"{len(team_ids)=}."
        )

        if preview:
            continue

        num_attempts = 3
        for attempt_count in range(num_attempts):
            try:
                api.orgs.create_invitation(
                    org=dest_org,
                    invitee_id=user_id,
                    team_ids=list(team_ids),
                )
            # Might have hit a secondary rate limit
            # https://docs.github.com/en/rest/overview/resources-in-the-rest-api#secondary-rate-limits
            except HTTP403ForbiddenError as http403:
                if attempt_count == attempt_count - 1:
                    click.echo("  got a 403. Max attempts reached; will raise.")
                    raise
                if "Retry-After" in http403.headers:
                    wait_seconds = http403.headers["Retry-After"] + 1
                    click.echo(
                        "  got a 403. Based on Retry-After header, will retry in "
                        f"{wait_seconds}s."
                    )
                else:
                    wait_seconds = 3
                    click.echo(
                        "  got a 403. No Retry-After header; will retry in "
                        f"{wait_seconds}s."
                    )
                time.sleep(wait_seconds)

    for index, username in enumerate(requested_users_already_in_org):
        teams_for_user = user_to_teams[username]
        click.echo(
            f"({index:03d}/{len(requested_users_already_in_org)}) updating teams for "
            f"user {username}; {len(teams_for_user)=}."
        )

        if preview:
            continue

        for team in teams_for_user:
            api.teams.add_or_update_membership_for_user_in_org(
                org=dest_org,
                team_slug=team.slug,
                username=username,
                role=team.role,
            )


def extract_user_names(user_list_file) -> List[str]:
    """
    Load list of usernames, with comments (#-prefixed) stripped out.
    """
    comments_removed = [line.partition("#")[0] for line in user_list_file]
    stripped = [line.strip() for line in comments_removed]
    empty_lines_removed = [line for line in stripped if line]
    return empty_lines_removed


@dataclass(frozen=True)
class Team:
    """
    A class to represent the info weneed to know about each
    github team to be able to add a user to the team.
    """

    team_id: int
    slug: str
    role: str


def extract_merged_team_memberships(
    org_export_files: list,
    team_slugs_to_ids: Dict[str, int],
) -> Dict[str, Set[Team]]:
    """
    Given a list of handles to org export files, return a merged mapping of
    usernames to all teams they are members of.
    """
    # Build a mapping from usernames to team slugs.
    users_to_teams: Dict[str, Set[Team]] = defaultdict(set)

    for json_file in org_export_files:
        org_export_data = json.load(json_file)
        for team in org_export_data["teams"]:
            team_slug = team["slug"]

            member_team = Team(
                team_id=team_slugs_to_ids[team_slug],
                slug=team_slug,
                role="member",
            )
            maintainer_team = Team(
                team_id=team_slugs_to_ids[team_slug],
                slug=team_slug,
                role="maintainer",
            )

            # If the team is in multiple export files, we combine
            # them into one team for the destination org.
            for member in team["members"]:
                if maintainer_team in users_to_teams[member]:
                    continue
                    # because the user is already on the team with maintainer level access
                    # via another org.
                users_to_teams[member].add(member_team)

            for maintainer in team.get("maintainers", []):
                if member_team in users_to_teams[maintainer]:
                    users_to_teams[maintainer].remove(member_team)
                    # because we're gonna elevate this user's access

                users_to_teams[maintainer].add(maintainer_team)

    return users_to_teams


if __name__ == "__main__":
    migrate()  # pylint: disable=no-value-for-parameter
