"""
For all members of the org, give the member permission to a repo using
a team rather than directly.
"""

import json
from collections import defaultdict
from itertools import chain
from os import path

import click
from fastcore.net import HTTP404NotFoundError
from ghapi.all import GhApi, paged
from utils import access_level_to_string


def map_users_to_teams(org_data):
    """
    For a giver user name, provide a set of all teams they are on.
    """
    users_to_teams = defaultdict(set)
    for team in org_data["teams"]:
        for member in team["members"]:
            users_to_teams[member].add(team["slug"])

    # We do this because the default dict was nice for populating the data but
    # we don't want future lookups of users not in the list to succeed.
    # So we converet it back to a regular dict so key errors work as expected.
    return dict(users_to_teams)


def team_with_same_or_higher_level_access_for_repo(
    user, access_level, repo, teams_for_user
):
    for team in teams_for_user:
        if team in repo["team_access"] and repo["team_access"][team] >= access_level:
            return team

    return None


def get_or_create_access_team(api, org, repo, access_level, dry_run):
    # create a new team or get an existing matching team.
    # {repo_name}-{access-level}
    # add this repo to the team with the level of access the user has.

    access_string = access_level_to_string(access_level)
    if access_string == "pull":
        team_name = "pull-all"
    elif access_string == "push":
        team_name = "push-pull-all"
    else:
        team_name = f"{repo['name']}-{access_string}"
        description = "[Auto-created] Team created as a part of the effort to remove members direct access to repos."

    try:
        api.teams.get_by_name(org, team_name)
        click.secho(f"Team('{team_name}') already exists, reusing.")
    except HTTP404NotFoundError:
        click.secho(f"Creating {team_name}...", nl=False)
        if not dry_run:
            api.teams.create(org, team_name, description)
            api.teams.add_or_update_repo_permissions_in_org(
                org, team_name, org, repo["name"], access_string
            )
        click.secho("Done.")
    return team_name


@click.option("--org", default="openedx", help="The github org to update.")
@click.option(
    "--dry-run", "-n", default=False, is_flag=True, help="Make no actual changes."
)
@click.option(
    "--github-token",
    envvar="GITHUB_TOKEN",
    help="Personal access token that can add/remove/update teams and repo collaborators.",
)
@click.command()
def main(org, dry_run, github_token):
    api = GhApi()

    data_filename = f"migrate/export-{org}.json"
    if not path.exists(data_filename):
        raise Exception(
            f"No file found at location {data_filename}, you may need to run `python"
            "migrate/github_to_json.py {org}` first."
        )
    # load json data.
    org_data = json.loads(open(data_filename, "r").read())
    outside_collaborators = [
        user.login
        for user in chain.from_iterable(
            (paged(api.orgs.list_outside_collaborators, org))
        )
    ]

    # create a mapping of a user to their teams.
    users_to_teams = map_users_to_teams(org_data)
    # For each repo
    for repo in org_data["repos"]:
        for user, access_level in repo["user_access"].items():
            if user in outside_collaborators:
                continue
            team_with_higher_access = False
            if user in users_to_teams:
                team_with_higher_access = (
                    team_with_same_or_higher_level_access_for_repo(
                        user, access_level, repo, users_to_teams[user]
                    )
                )
            if team_with_higher_access:
                click.secho(
                    f"{user} has sufficient access to {repo['name']} via {team_with_higher_access}. "
                    "Removing direct access...",
                    nl=False,
                )
                # remove direct access
                if not dry_run:
                    api.repos.remove_collaborator(org, repo["name"], user)
                click.secho("Done.")
            else:  # we need a new team to capture the leval of access they need.
                access_team_slug = get_or_create_access_team(
                    api, org, repo, access_level, dry_run
                )
                click.secho(
                    f"Adding {user} to {access_team_slug} and removing direct access...",
                    nl=False,
                )
                # add user to team.
                if not dry_run:
                    api.teams.add_or_update_membership_for_user_in_org(
                        org, access_team_slug, user, "member"
                    )
                    api.repos.remove_collaborator(org, repo["name"], user)
                click.secho("Done.")


if __name__ == "__main__":
    main()
