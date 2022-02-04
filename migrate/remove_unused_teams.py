from pprint import pprint

import click
from cache_to_disk import cache_to_disk
from ghapi.all import GhApi, paged


@cache_to_disk(1)
def load_teams_data_from_github(org):
    """

    returns a Tuple of

    - fully_empty_teams: A list of team slugs of teams that have no members, repos, projects or
      sub_teams.
    - members_but_nothing_else: A list of team slugs for teams that have members but nothing else.
    - team_to_members: A mapping of team slugs to a list of team member logins.
    """
    api = GhApi()

    # Get teams and their related artifacts.
    teams = []
    fully_empty_teams = []
    members_but_nothing_else = []
    team_to_members = {}
    for page in paged(api.teams.list, org, per_page=100):
        teams.extend(page)

    for team in teams:
        # we ignore the fact that there could be multiple pages of responses because we don't need
        # a full list of teams, since we're just looking for the teams that don't have any of these
        # objects.
        repos = api.teams.list_repos_in_org(org, team.slug)
        projects = api.teams.list_projects_in_org(org, team.slug)
        child_teams = api.teams.list_child_in_org(org, team.slug)

        # We get all the team members so we can review teams that still
        # have members.
        team_members = []
        for page in paged(api.teams.list_members_in_org, org, team.slug):
            team_members.extend(page)

        team_to_members[team.slug] = [member.login for member in team_members]
        if len(repos) == 0 and len(projects) == 0 and len(child_teams) == 0:
            if len(team_members) == 0:
                fully_empty_teams.append(team.slug)
            else:
                members_but_nothing_else.append(team.slug)
    return (fully_empty_teams, members_but_nothing_else, team_to_members)


@click.option(
    "--org", default="openedx", help="The github org that you wish to cleanup."
)
@click.option(
    "--dry-run",
    "-n",
    default=False,
    is_flag=True,
    help="Show what changes would be made without making them.",
)
@click.command()
def main(org, dry_run):
    deletion_count = 0
    api = GhApi()
    (
        fully_empty_teams,
        members_but_nothing_else,
        team_to_members,
    ) = load_teams_data_from_github(org)

    click.secho(
        "The following teams have no related repos, projects, members, or child teams:",
        bold=True,
    )
    click.secho("    - ", nl=False, fg="red")
    click.secho("\n    - ".join(fully_empty_teams), fg="red")

    if len(fully_empty_teams) > 0 and (
        dry_run or click.confirm("Delete all fully empty teams?")
    ):
        click.secho("Deleting fully empty teams.", bold=True, fg="red")
        # TODO: Actually do the deletion here.
        for team in fully_empty_teams:
            click.secho(f"Deleting '{team}'...", nl=False, fg="red")
            if not dry_run:
                api.teams.delete_in_org(org, team)
            click.secho(f"Done", fg="red")
            deletion_count += 1

    for team in members_but_nothing_else:
        click.secho(f"'{team}' has the following members:", bold=True)
        click.secho("    - ", nl=False)
        click.secho("\n    - ".join(team_to_members[team]))

        if dry_run or click.confirm(f"Delete '{team}'?"):
            click.secho(f"Deleting '{team}'...", nl=False, fg="red")
            if not dry_run:
                api.teams.delete_in_org(org, team)
            click.secho(f"Done", fg="red")
            deletion_count += 1

    click.echo("\n\n")
    click.echo(click.style(f"{deletion_count}", bold=True) + " teams deleted.")


if __name__ == "__main__":
    main()
