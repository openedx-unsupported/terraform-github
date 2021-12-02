#!/usr/bin/env python3
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments,too-many-locals,too-many-branches,too-many-statements

# No mypy stubs for fastcore or ghapi; just turn off type-checking.
# type: ignore

import json
import os
import sys
from typing import Dict, List, Set

import click
from fastcore.net import \
    HTTP404NotFoundError  # pylint: disable=no-name-in-module
from ghapi.all import GhApi, paged


@click.command()
@click.argument("src_org")
@click.argument("dest_org")
@click.argument("export_json_file", type=click.File("r"))
@click.option(
    "--username",
    help=(
        "As the user making create requests, you are added to all teams automatically. "
        "Provide your username to ensure that you are removed from those teams."
    ),
)
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
    "--description-prefix",
    help="Optional prefix for migrated team descriptions.",
    default="",
)
def migrate(
    src_org: str,
    dest_org: str,
    export_json_file,
    username: str,
    preview: bool,
    no_prompt: bool,
    description_prefix: str,
):
    """
    Migrate GH team 'shells' (empty teams with names & descriptions, but no members).

    Migrates the teams in {export_json_file} from from {src_org} to {dest_org}.
    Fails early if any of the teams don't exist in {src_org}.
    Teams are created or updated in {dest_org}. The operation should be idempotent.
    Migrated data includes:
    * name,
    * slug (GH calculates this deterministically from the name), and
    * description, prefixed with {description_prefix} if provided.

    {export_json_file} is expected to have this format:
        {
            "teams": [
                {
                    "slug": "slug-of-team-to-migrate",
                    ...other fields
                },
                {
                    "slug": "slug-of-another-team-to-migrate",
                    ...other fields
                },
                ...more teams
            ]
            ...other fields
        }
    """
    # The set of source organization owners is grouped into a team.
    # The team will later be granted admin rights on all migrated repos.
    # This allows us to retain their repo permissions without needing to
    # grant
    admin_team_slug = f"{src_org}-admin"

    if preview:
        click.secho("In Preview Mode: No changes will be made!", italic=True)
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        sys.exit("Fatal Error: Please set a GITHUB_TOKEN environment variable.")

    teams: List[dict] = json.load(export_json_file)["teams"]
    team_slugs: List[str] = list(sorted(team["slug"] for team in teams))
    click.echo(f"Read {len(team_slugs)} teams from {export_json_file.name}")
    if not team_slugs:
        sys.exit("No teams to migrate. Quitting.")

    api = GhApi(token=github_token)

    click.echo(f"Loading metadata on {len(team_slugs)} teams...")
    team_slugs_in_dest_org: Set[str] = set(
        team.slug
        for page in paged(api.teams.list, dest_org, per_page=100)
        for team in page
    )
    team_info_by_slug: Dict[str, Dict] = {}
    for team_slug in team_slugs:
        team_info: Dict = {}
        try:
            api_team_data = api.teams.get_by_name(src_org, team_slug)
            team_info["name"] = api_team_data["name"]
            prefix_string = description_prefix + " " if description_prefix else ""
            team_info["description"] = prefix_string + api_team_data["description"]
        except HTTP404NotFoundError:
            if team_slug == admin_team_slug:
                team_info["name"] = team_slug
                team_info["description"] = (
                    f"Users who were owners of the {src_org} GitHub organization "
                    f"at the time of migration to the {dest_org} GitHub organization."
                )
            else:
                sys.exit(
                    f"  Team {team_slug!r} does not exist in source org "
                    f"{src_org!r}. Quitting."
                )
        team_info_by_slug[team_slug] = team_info
        action_verb = "update" if team_slug in team_slugs_in_dest_org else "create"
        click.echo(f"  must {action_verb} team {team_info['name']!r}")

    num_to_create = len(set(team_slugs) - team_slugs_in_dest_org)
    num_to_update = len(team_slugs) - num_to_create
    click.echo()
    click.secho(
        f"Will create {num_to_create} teams and update {num_to_update} teams "
        f"from {src_org!r} into {dest_org!r}.",
        bold=True,
    )

    if not no_prompt:
        click.echo()
        click.confirm("Proceed?", abort=True)

    with click.progressbar(
        team_info_by_slug.items(),
        label=f"Mirroring teams from org {src_org!r} into org {dest_org!r}",
    ) as progress_bar:

        for team_slug, team_info in progress_bar:

            create_new = team_slug not in team_slugs_in_dest_org
            click.echo(f" {'create' if create_new else 'update'}: {team_slug}")
            if preview:
                continue

            # Note: the Teams API is a little ambiguous w.r.t. 'name' versus
            # 'slug'. A 'slug' is a url-safe, lowercase string calculated from
            # the team name, whereas the team name can contain spaces, symbols, etc.
            # That is why we *create* a team using the name, but *update*
            # using the slug as an identifier. Changing the name will always
            # update the underlying slug, so
            # it is always the case that ``team.slug == slugify(team.name)``.

            if create_new:
                api.teams.create(
                    org=dest_org,
                    name=team_info["name"],  # team_slug will be inferred from name.
                    description=team_info["description"],
                    privacy="closed",
                )
                # The API user is automatically added to the team, so we need to
                # specifically remove them after the team is created.
                api.teams.remove_membership_for_user_in_org(
                    org=dest_org, team_slug=team_slug, username=username
                )
            else:
                api.teams.update_in_org(
                    org=dest_org,
                    team_slug=team_slug,
                    name=team_info["name"],
                    description=team_info["description"],
                    privacy="closed",
                )


if __name__ == "__main__":
    migrate()  # pylint: disable=no-value-for-parameter
