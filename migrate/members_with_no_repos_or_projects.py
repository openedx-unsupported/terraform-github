from itertools import chain
from typing import Dict, List

import click
from cache_to_disk import cache_to_disk
from ghapi.all import GhApi, paged


@cache_to_disk(1)
def get_members_with_repo_access(api, org):
    repos = list(chain.from_iterable(paged(api.repos.list_for_org, org, per_page=100)))
    members_with_repo_access = set()
    with click.progressbar(
        repos, label="Finding members with repo access"
    ) as repos_with_progress:
        for repo in repos_with_progress:
            collaborators = chain.from_iterable(
                paged(api.repos.list_collaborators, org, repo.name, per_page=100)
            )
            for collaborator in collaborators:
                members_with_repo_access.add(collaborator.login)
    return members_with_repo_access


@cache_to_disk(1)
def get_members_with_project_access(api, org):
    projects = list(
        chain.from_iterable(paged(api.projects.list_for_org, org, per_page=100))
    )
    members_with_project_access = set()
    with click.progressbar(
        projects, label="Finding members with project access."
    ) as projects_with_progress:
        for project in projects_with_progress:
            collaborators = chain.from_iterable(
                paged(api.projects.list_collaborators, project.id, per_page=100)
            )
            for collaborator in collaborators:
                members_with_project_access.add(collaborator.login)
    return members_with_project_access


@click.command()
@click.option(
    "--github-token",
    envvar="GITHUB_TOKEN",
    required=True,
    help="A github personal access token.",
)
@click.option(
    "--org",
    default="openedx",
    help="The github organization to introspect.",
)
@click.option("--refresh-cache", default=False, is_flag=True)
def main(org, github_token, refresh_cache):
    """
    List all users that don't have access to any repos or projects but still
    are members of the org.  These may be candidates for removal from the org.

    This script is read-only and will not make any changes to your org.
    """

    api = GhApi()
    if refresh_cache:
        get_members_with_repo_access.cache_clear()
        get_members_with_project_access.cache_clear()

    members = {
        m.login
        for m in chain.from_iterable(paged(api.orgs.list_members, org, per_page=100))
    }

    members_with_repo_access = get_members_with_repo_access(api, org)
    members_with_project_access = get_members_with_project_access(api, org)

    members_with_no_projects_or_repos = (
        members - members_with_repo_access - members_with_project_access
    )

    click.secho("Members with no repo or project access:")
    for member in sorted(members_with_no_projects_or_repos):
        click.secho(f"    - {member}")


if __name__ == "__main__":
    main()
