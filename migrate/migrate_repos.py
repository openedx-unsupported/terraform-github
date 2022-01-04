# pylint: disable=missing-module-docstring,missing-function-docstring,too-many-arguments
"""
Script for migrating repositories across GitHub organizations.
"""
# pylint: disable=missing-function-docstring
from collections import defaultdict
from typing import Dict, List
import dataclasses
import json
import itertools
import os
import sys
import time
from urllib.error import HTTPError

import click
from ghapi.all import GhApi, paged  # type: ignore


MAX_PAGE_SIZE = 100  # This is GitHub's page size limit


@click.command()
@click.argument("src_org")
@click.argument("dest_org")
@click.argument("repo_list_file", type=click.File("r"))
@click.option(
    "--preview", is_flag=True, help="Preview what will happen but don't execute."
)
@click.option(
    "--skip-missing-repos",
    is_flag=True,
    help=(
        "Skip repos that are not found in the source org, instead of failing. "
        "Useful after an error."
    ),
)
@click.option(
    "--skip-missing-teams",
    is_flag=True,
    help=("Skip missing teams instead of failing. Use with caution."),
)
@click.option(
    "--no-prompt",
    is_flag=True,
    help="Don't ask for a confirmation before transferring the repos.",
)
@click.option(
    "--permissions-file",
    type=click.File(),
    help="JSON file with repos to teams/user permissions mappings.",
)
@click.option(
    "--github-token",
    envvar="GITHUB_TOKEN",
    show_default="$GITHUB_TOKEN environment variable.",
)
@click.option(
    "--resume-from",
    help="Name of the repo to resume from. Used after a transfer has failed partway through."
)
def migrate(
    src_org,
    dest_org,
    repo_list_file,
    preview,
    skip_missing_repos,
    skip_missing_teams,
    no_prompt,
    permissions_file,
    github_token,
    resume_from,
):
    """
    Migrate repositories from SRC_ORG to DEST_ORG.
    """
    show_prompts = not no_prompt  # It just makes it clearer in later code.
    if preview:
        click.secho("In Preview Mode: No changes will be made!", italic=True)

    # Basic validation: We need a GITHUB_TOKEN for the API
    if not github_token:
        sys.exit(
            "Fatal Error: Set your $GITHUB_TOKEN environment variable or specify it using --github-token"
        )

    # Basic validation: Doesn't make sense to transfer within the same org.
    if src_org == dest_org:
        sys.exit("Fatal Error: Source and destination orgs must be different.")

    # Optional validation: You don't absolutely need teams specified to move a
    # set of repos (maybe there's just one and the team assigned to it doesn't
    # matter, e.g. edx-solutions repos that we're not importing team data from).
    # But it's probably a good idea to double check.
    if show_prompts and not permissions_file:
        click.echo(
            "You haven't specified a team/user to repos permissions file (--permissions-file)."
        )
        click.secho(
            "WARNING: Repos will be copied over with NO team/user permissions set!",
            bold=True,
        )
        click.confirm("Proceed anyway?", abort=True)

    # We passed the most basic input validations.
    # Get the list of repos from our text file.
    repos_to_transfer = extract_repo_names(repo_list_file, resume_from)
    click.echo(f"Read {len(repos_to_transfer)} repos from {repo_list_file.name}")

    # Initialize the GitHub API client
    api = GhApi(token=github_token)

    # Basic sanity check to make sure the repos we're transferring all actually exist.
    click.echo(f"Fetching the list of repos in source org {src_org}...")
    src_org_repos = {
        repo["name"]
        for repo in itertools.chain.from_iterable(
            paged(api.repos.list_for_org, src_org, per_page=MAX_PAGE_SIZE)
        )
    }

    missing_repos = [repo for repo in repos_to_transfer if repo not in src_org_repos]

    # Have we already transferred the repo we're supposed to resume from?
    resume_from_repo_already_transferred = missing_repos and (missing_repos == [resume_from])

    if resume_from_repo_already_transferred:
        # Mostly likely reason we're here is because the repo transfer succeeded
        # in a previous run, but there was an error applying permissions right
        # afterwards.
        click.echo(
            f"The {resume_from} repo is not in the source org (probably alredy "
            + "transerred?). We will re-apply team permissions to it."
        )
    elif missing_repos:
        if skip_missing_repos:
            click.echo(
                f"The following repositories are missing from {src_org} and will be skipped:"
            )
            for missing_repo in missing_repos:
                click.echo(f"- {missing_repo}")

            # Filter out the repos that we've asked to transfer but aren't present in the
            # org that we're transferring them from.
            repos_to_transfer = [
                repo for repo in repos_to_transfer if repo in src_org_repos
            ]
        else:
            # If skip_missing_repos isn't specified, treat missing repos as an error.
            # (Maybe they're trying to move things from the wrong org.)
            sys.exit(
                "Fatal Error: The following repos marked for transfer are not in "
                f"org {src_org}: {', '.join(missing_repos)}"
            )

    if not repos_to_transfer:
        sys.exit("No repos to transfer. Quitting.")

    # Check permissions file
    if permissions_file:
        repos_to_permissions = load_permissions(
            permissions_file, api, dest_org, skip_missing_teams
        )

        # Validation: Make sure we have permissions entries for all the repos
        # that we're transferring over.
        repos_with_no_permissions = [
            repo for repo in repos_to_transfer if repo not in repos_to_permissions
        ]
        if repos_with_no_permissions:
            sys.exit(
                "Fatal Error: --permissions-file was specified, but the "
                + "following repos have no permissions entries: "
                + ", ".join(repos_with_no_permissions)
            )
    else:
        repos_to_permissions = {}

    if show_prompts:
        click.echo()
        click.secho(
            f"The following {len(repos_to_transfer)} "
            f"repositories will be moved from {src_org} to {dest_org}: ",
            nl=False,
            bold=True,
        )
        click.echo(", ".join(repos_to_transfer))
        click.echo()
        click.confirm("Proceed?", abort=True)

    # Do the actual transfer
    click.echo()
    click.echo(
        f"Transferring {len(repos_to_transfer)} repositories from {src_org} to {dest_org}..."
    )

    for (i, repo) in enumerate(repos_to_transfer, start=1):
        click.secho(f"{i:>3}: {repo}", bold=True)
        if not preview:
            # Special case handling: Don't transfer the repo if it's the resume_from
            # repo that was already transferred (but had borked permissions).
            skip_transfer = resume_from_repo_already_transferred and (repo == resume_from)

            if not skip_transfer:
                # Do the actual repo transfer call.
                api.repos.transfer(src_org, repo, dest_org)

                # Without this sleep, we'll sometimes hit a race condition where the
                # repo would not have been recognized as transferred before the
                # permissions code tried to run, leading to errors because the repo
                # did not exist at the new location yet. Need to put something more
                # robust here (auto-retry?) later.
                time.sleep(2)

        if repos_to_permissions:
            permissions = repos_to_permissions[repo]
            set_repo_permissions(permissions, api, dest_org, preview)


@dataclasses.dataclass(frozen=True)
class RepoPermissions:
    """
    Permissions for a particular repository.
    """

    slug: str              # Name of the repo
    teams: Dict[str, str]  # Mapping of team slug to permission slug
    users: Dict[str, str]  # Mapping of username to permission slug

    @classmethod
    def parse_from_file_entry(cls, repo_data):
        access_level_mapping = {
            1: "pull",
            2: "push",
            3: "maintain",
            4: "admin",
        }
        return cls(
            slug=repo_data["name"],
            teams={
                team_slug: access_level_mapping[access_level]
                for team_slug, access_level in repo_data["team_access"].items()
            },
            users={
                username: access_level_mapping[access_level]
                for username, access_level in repo_data["user_access"].items()
            },
        )


def extract_repo_names(repo_list_file, resume_from):
    comments_removed = [line.partition("#")[0] for line in repo_list_file]
    stripped = [line.strip() for line in comments_removed]
    empty_lines_removed = [line for line in stripped if line]
    if resume_from:
        # If we're passed a repo name to resume from, we'll ignore all the ones
        # leading up to it.
        final_repo_list = list(
            itertools.dropwhile(
                lambda repo: repo != resume_from, empty_lines_removed
            )
        )
        if not final_repo_list:
            sys.exit(
                f"Fatal Error: --resume-from={resume_from} was specified, but "
                + f"{resume_from} not found in repo list: \n  "
                + ",".join(empty_lines_removed)
            )
        click.echo(f"Resuming transfer from repo {resume_from}")
    else:
        final_repo_list = empty_lines_removed

    return final_repo_list


def load_permissions(teams_file, api, dest_org, skip_missing_teams):
    """
    Return a dict mapping of team_slug to RepoPermissions.

    These include the team permissions we're planning to apply. If
    skip_missing_teams is True, we'll strip out all missing teams and users
    from the returned RepoPermissions objects.
    """
    click.echo(f"Fetching known teams from {dest_org}...")
    known_team_slugs = {
        team["slug"]: team["id"]
        for team in itertools.chain.from_iterable(
            paged(api.teams.list, dest_org, per_page=MAX_PAGE_SIZE)
        )
    }
    click.echo(f"-> Found {len(known_team_slugs)} teams.")

    click.echo(f"Fetching known users from {dest_org}...")
    known_usernames = {
        user["login"]: user["id"]
        for user in itertools.chain.from_iterable(
            paged(api.orgs.list_members, dest_org, per_page=MAX_PAGE_SIZE)
        )
    }
    click.echo(f"-> Found {len(known_usernames)} usernames.")

    click.echo(f"Reading desired team and user permissions from {teams_file.name}...")
    repos_to_permissions = {
        repo_data["name"]: RepoPermissions.parse_from_file_entry(repo_data)
        for repo_data in json.load(teams_file)["repos"]
    }

    # Do we have any teams that are missing from the destination org?
    missing_teams_to_repos = defaultdict(list)
    missing_usernames_to_repos = defaultdict(list)

    for permissions in repos_to_permissions.values():
        repo = permissions.slug
        for team in permissions.teams:
            if team not in known_team_slugs:
                missing_teams_to_repos[team].append(repo)
        for username in permissions.users:
            if username not in known_usernames:
                missing_usernames_to_repos[username].append(repo)

    if missing_teams_to_repos or missing_usernames_to_repos:
        click.echo(
            "Error: There are references to teams or users in "
            + f"{teams_file.name} that do not exist in destination org {dest_org}: "
        )

        if missing_teams_to_repos:
            click.echo("Missing Teams:")
            for team in sorted(missing_teams_to_repos):
                repos_team_is_used_in = sorted(missing_teams_to_repos[team])
                click.secho(f"  {team}", bold=True, nl=False)
                click.echo(f" used in {', '.join(repos_team_is_used_in)}")

        if missing_usernames_to_repos:
            click.echo("Missing Users:")
            for username in sorted(missing_usernames_to_repos):
                repos_user_is_used_in = sorted(missing_usernames_to_repos[username])
                click.secho(f"  {username}", bold=True, nl=False)
                click.echo(f" used in {', '.join(repos_user_is_used_in)}")

        if skip_missing_teams:
            click.secho("Ignoring missing teams and users!", bold=True)
            # Return a modified version of repos_to_permissions that has the
            # missing information stripped out.
            stripped_repos_to_permissions = {}
            for repo, permissions in repos_to_permissions.items():
                stripped_repos_to_permissions[repo] = dataclasses.replace(
                    permissions,
                    teams={team: role for team, role in permissions.teams.items() if team in known_team_slugs},
                    users={username: role for username, role in permissions.users.items() if username in known_usernames}
                )
            return stripped_repos_to_permissions
        else:
            sys.exit(
                "Exiting because teams or users are missing. "
                "To ignore this check, use --skip-missing-teams"
            )

    return repos_to_permissions


def set_repo_permissions(permissions, api, dest_org, preview):
    """
    Set team permissions for one repo.

    Won't actually make any GitHub API calls if preview is True.

    The permissions param is a dict of repo slugs to RepoPermissions objects.

    This function only sets team permissions and not user permissions. User
    roles will follow over with the transferred repository–there's no need to
    set them manually here.
    """
    # teams_by_role is a mapping of access role (e.g. "admin") to a list of
    # team slugs.
    teams_by_role = defaultdict(list)
    for team_slug, access in sorted(permissions.teams.items()):
        teams_by_role[access].append(team_slug)

    # The permissions update call requires that the owner be specified, but the
    # owner for a repo in an org is just the user that has the login of the org
    # name (verified by looking through the results of getting repo listings
    # from this API). So everything in the org "openedx" is owned by user
    # "openedx".
    owner = dest_org

    for access, teams in sorted(teams_by_role.items()):
        click.secho(f"     assigning {access} teams:", italic=True)
        click.echo("      ", nl=False)
        for team_slug in teams:
            click.echo(f" {team_slug}", nl=False)
            if not preview:
                api.teams.add_or_update_repo_permissions_in_org(
                    org=dest_org,
                    team_slug=team_slug,
                    owner=owner,
                    repo=permissions.slug,
                    permission=access,
                )
        click.echo()


if __name__ == "__main__":
    try:
        migrate()  # pylint: disable=no-value-for-parameter
    except HTTPError as http_error:
        click.echo(f"Exception url: {http_error.url}")
        click.echo(f"Exception body: {http_error.fp.read()}")
        raise
