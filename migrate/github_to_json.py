#!/usr/bin/env python3
"""
Load GH teams, specified repos, and user/team permissions on those repos.

Dumps JSON to migrate/export-$ORGANIZATION.json. Logs progess to stderr.

Usage:
    python -m migrate.github_to_json.py ORGANIZATION
Or just:
    make migrat-github-to-json

Requirement installation:
    make migrate-requirements  # in a virtualenv, from repo root

Other requirements:
    * Python >=3.8
    * Expects a personal GH access token in the environment as GITHUB_TOKEN.
      (The token needs owner-level read access to ORGANIZATION.)
    * Expects list of repo names for transfer at
      `migrate/repos-ORGANIZATION.txt`.

Linting:
    make migrate-requirements-dev  # in a virtualenv, from repo root
    make migrate-lint
"""

# pylint: disable=unspecified-encoding
import json
import logging
import os
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, List, Set

import github as gh_api
import requests
from github.Organization import Organization as ApiOrganization
from github.Permissions import Permissions as ApiPermissions

from .utils import (
    REPO_ADMIN,
    REPO_MAINTAIN,
    REPO_NONE,
    REPO_READ,
    REPO_WRITE,
    RepoAccessLevel,
    RepoName,
    TeamSlug,
    Username,
)

# While iteratively develping, you might use a limited set of repos & teams
# to speed up test runs and/or avoid getting rate-limited by GitHub
DEBUG_TEAM_SLUG_PREFIX = ""
DEBUG_REPO_NAME_PREFIX = ""

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
LOG = logging.getLogger(__name__)


def main():
    """
    Script entrypoint
    """
    assert len(sys.argv) == 2, "Expected one arg: ORGANIZATION"
    org_slug = sys.argv[1]

    LOG.info("Fetching organization repos, teams, and permissions from GitHub API.")
    repo_names = get_repo_names_to_move(org_slug)
    gh_token = get_github_token()

    LOG.info(" Authenticating.")
    gh_client = gh_api.Github(gh_token)
    org = gh_client.get_organization(org_slug)
    LOG.info(" Authenticated.")

    # set up HTTP headers because PyGithub isn't able to determine team permissions
    # on a repo in bulk.
    gh_headers = {"AUTHORIZATION": f"token {gh_token}"}

    teams = fetch_teams(gh_headers, org)
    repo_permissions = fetch_repo_permissions(gh_headers, org, repo_names, teams)

    LOG.info("Done fetching.")

    results = {
        "export_date_utc": datetime.utcnow().isoformat(),
        "repos": [asdict(repo) for repo in repo_permissions],
        "teams": [asdict(team) for team in teams],
    }
    with open(f"migrate/export-{org_slug}.json", "w") as export_file:
        print(json.dumps(results, indent=4), file=export_file)


@dataclass(frozen=True)
class Repo:
    """
    A repository, including users' and teams' access levels to it.
    """

    name: RepoName
    user_access: Dict[Username, RepoAccessLevel]
    team_access: Dict[TeamSlug, RepoAccessLevel]


@dataclass(frozen=True)
class Team:
    """
    A team and its members.

    The 'slug' is the thing you mention the team with, without the org prefix.
    Example: the team @edx/teaching-and-learning has the slug 'teaching-and-learning'.
    This is distinct from the name, whic ph can contain spaces (eg 'Teaching & Learning').
    """

    slug: TeamSlug
    maintainers: List[Username]
    members: List[Username]


def fetch_repo_permissions(
    gh_headers: dict,
    org: ApiOrganization,
    repo_names: List[RepoName],
    teams: List[Team],
) -> List[Repo]:
    """
    Load repos with associated user/team permissions.

    The general strategy here is:
    * For each repo,
      * find teams' access levels to the repo via GH API,
      * find users' effective access levels to the repo via GH API,
        * and use this info to deduce users' *directly-granted* repo access.
    """
    # pylint: disable=too-many-locals

    team_members: Dict[TeamSlug, Set[Username]] = {
        team.slug: set(team.maintainers + team.members) for team in teams
    }

    LOG.info(" Fetching metadata for all repos in org.")
    api_repos = org.get_repos()
    repos = []

    LOG.info(" Fetching permissions for individual repos.")
    for api_repo in sorted(api_repos, key=lambda api_repo: api_repo.name):

        # Skip repos that we're not interested in.
        repo_name = RepoName(api_repo.name)
        if repo_name not in repo_names:
            LOG.info("  Skipping repo %s; not in transfer list.", repo_name)
            continue
        if not repo_name.startswith(  # pylint: disable=no-member
            DEBUG_REPO_NAME_PREFIX
        ):
            LOG.info("  Skipping repo %s; excluded for debugging.", repo_name)
            continue

        LOG.info("  Fetching permissions for repo %s.", repo_name)

        # For this repo, we now want a build a mapping from teams to access
        # levels.
        team_access: Dict[TeamSlug, RepoAccessLevel] = {}
        # Unfortunately, the GitHub API returns *effective* user-repo access,
        # not *direct* user-repo access. That is, `collaborator.permissions`
        # includes permissions granted via teams AND permissions granted directly
        # to the user.
        # So, to calculate `user_access` (that is, determine which permissions are
        # assigned directly to the user), we must reverse engineer it: we
        # figure out what access is granted to each user via teams, and then take
        # the 'difference' of `effective_user_access` and `user_access`.
        user_access_via_teams: Dict[Username, RepoAccessLevel] = defaultdict(
            lambda: REPO_NONE
        )

        # Handle org admin team.
        # Recall from fetch_teams that this is a team we invented in order to
        # capture the users who currently have owner permissions on the org.
        # Members of this team get admin access to all imported repositories.
        admin_team_slug = get_admin_team_slug(org.login)
        team_access[admin_team_slug] = REPO_ADMIN
        for admin_username in team_members[admin_team_slug]:
            user_access_via_teams[admin_username] = REPO_ADMIN

        # Fetch teams associated with repository from GitHub API.
        LOG.info("   Fetching team permissions.")
        teams_response = requests.get(api_repo.teams_url, headers=gh_headers)
        assert teams_response.status_code == 200
        teams_data = teams_response.json()
        assert isinstance(teams_data, list)

        # Populate team_access and user_access_via_team mappings based on
        # teams returned from repository-teams-lsiting API.
        for team_data in sorted(teams_data, key=lambda t: t["slug"]):
            team_slug = team_data["slug"]
            team_access[team_slug] = normalize_access_level(team_data["permissions"])
            if not DEBUG_TEAM_SLUG_PREFIX:
                # If the team is missing from the team_members map, something has
                # gone wrong.
                assert team_slug in team_members, (
                    f"Internal error! Team {team_slug!r} has access to {repo_name!r}, "
                    "but we didn't record its membership."
                )
            for username in team_members.get(team_slug, []):
                user_access_via_teams[username] = max(
                    team_access[team_slug],
                    user_access_via_teams[username],
                )

        # For this repo, we now want a build a mapping from users to access
        # levels. As previously noted, the GitHub API returns *effective* user
        # access, so we will compute user_access as (roughly):
        #   user_access = effective_user_access - user_access_via_teams
        user_access: Dict[Username, RepoAccessLevel] = {}
        effective_user_access: Dict[Username, RepoAccessLevel] = {}

        # Fetch users associated with repository from GitHub API.
        LOG.info("   Fetching collaborator permissions.")
        api_users = list(api_repo.get_collaborators())

        for api_user in sorted(api_users, key=lambda u: u.login):
            username = Username(api_user.login)
            effective_user_access[username] = normalize_access_level(
                api_user.permissions
            )
            # Record a user_access entry iff the access granted via teams
            # is lower the user's effective access.
            if user_access_via_teams[username] < effective_user_access[username]:
                user_access[username] = effective_user_access[username]
            # Sanity check: it'd make no sense for a user to have a level of access via
            # a team, but then have *lower* level of effective access.
            assert user_access_via_teams[username] <= effective_user_access[username], (
                "Internal error! "
                f"W.r.t {username} in {repo_name}, "
                f"effective access level is {effective_user_access[username]:}, "
                f"and team-granted access level is {user_access_via_teams[username]}. "
                "However, we expect that effective access "
                "is always >= than team-granted access."
            )

        # Just a sanity check: for every user that had access via teams, we should
        # have found (in the loop above) that they had effective access.
        usernames_with_team_but_not_eff_access = set(user_access_via_teams) - set(
            effective_user_access
        )
        assert not usernames_with_team_but_not_eff_access, (
            "Internal error! There are users who should have access to a "
            "repository via team-granted permissions, but they are not "
            "reflected in the list of repository collaborators. Users: "
            f"{usernames_with_team_but_not_eff_access}."
        )

        # Done with this repo!
        LOG.info("  Done with repo %s", repo_name)
        repos.append(
            Repo(
                name=repo_name,
                user_access=user_access,
                team_access=team_access,
            )
        )

    LOG.info(" Done fetching .")
    return repos


def normalize_access_level(access) -> RepoAccessLevel:
    """
    The GitHub API expresses permissions in a few different ways :/

    Here's our best attempt at normalizing them.
    """
    # pylint: disable=too-many-return-statements,too-many-branches
    if isinstance(access, ApiPermissions):
        if access.admin:
            return REPO_ADMIN
        if access.maintain:
            return REPO_MAINTAIN
        if access.push:
            return REPO_WRITE
        if access.pull:
            return REPO_READ
        return REPO_NONE
    if isinstance(access, dict):
        if access["admin"]:
            return REPO_ADMIN
        if access["maintain"]:
            return REPO_MAINTAIN
        if access["push"]:
            return REPO_WRITE
        if access["pull"]:
            return REPO_READ
        return REPO_NONE
    if isinstance(access, str):
        if access in ["admin"]:
            return REPO_ADMIN
        if access in ["maintain"]:
            return REPO_MAINTAIN
        if access in ["write", "push"]:
            return REPO_WRITE
        if access in ["read", "pull"]:
            return REPO_READ
        raise ValueError(f"bad repo access string: {access!r}")
    raise TypeError(f"bad access level object: {access!r}")


def fetch_teams(gh_headers: dict, org: ApiOrganization) -> List[Team]:
    """
    Load teams and members.
    """

    # We treat org owners as team with admin permissions on all org repos,
    # because we don't necessarily want to make them owners in the openedx org.
    LOG.info(" Fetching list of organization owners.")
    members_url = org.members_url.split("{")[0]
    admins_url = f"{members_url}?role=admin&per_page=100"
    admin_user_response = requests.get(admins_url, headers=gh_headers)
    assert admin_user_response.status_code == 200
    assert isinstance(admin_user_response.json(), list)
    admin_team = Team(
        slug=get_admin_team_slug(org.login),
        # Only destination org owners will be allowed to manage this team.
        maintainers=[],
        members=sorted(
            Username(admin_user_data["login"])
            for admin_user_data in admin_user_response.json()
        ),
    )

    LOG.info(" Fetching list of teams in organization.")
    api_teams = list(org.get_teams())
    teams = [admin_team]

    for api_team in sorted(api_teams, key=lambda api_team: api_team.slug):
        team_slug = TeamSlug(api_team.slug)
        if not team_slug.startswith(  # pylint: disable=no-member
            DEBUG_TEAM_SLUG_PREFIX
        ):
            LOG.info("  Skipping team %s; excluded for deugging.", team_slug)
            continue

        LOG.info("  Fetching members for team %s.", team_slug)
        maintainers = {
            # Maintainers are special team members that can modify membership, settings, etc.
            # In addition to any team members that are explicitly marked as maintainers,
            # any and all organization owners on the team will implicitly be considered
            # maintainers instead of normal team members.
            Username(user.login)
            for user in api_team.get_members(role="maintainer")
        }
        members = {
            # By specifying role='member' in the API call, we exclude maintainers,
            # instead only including the remaining "normal" team members.
            Username(user.login)
            for user in api_team.get_members(role="member")
        }
        team = Team(
            slug=team_slug,
            members=sorted(members),
            maintainers=sorted(maintainers),
        )
        teams.append(team)

    LOG.info(" Done fetching team members.")
    return teams


def get_github_token() -> str:
    """
    Load GH persoal access token from file.
    """
    return os.environ["GITHUB_TOKEN"]


def get_repo_names_to_move(org_slug: str) -> Set[RepoName]:
    """
    Load repo names from file.
    """
    with open(f"migrate/repos-{org_slug}.txt") as repos_file:
        return set(RepoName(line.strip()) for line in repos_file.readlines())


def get_admin_team_slug(org_slug: str) -> TeamSlug:
    """
    Given org name (slug), return the name of the new team that'll contain its owners.
    """
    return TeamSlug(f"{org_slug}-admin")


if __name__ == "__main__":
    main()
