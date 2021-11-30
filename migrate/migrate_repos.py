# pylint: disable=missing-module-docstring,missing-function-docstring
import itertools
import os
import sys

import click
from ghapi.all import GhApi, paged  # type: ignore


@click.command()
@click.argument("src_org")
@click.argument("dest_org")
@click.argument("repo_list_file", type=click.File("r"))
@click.option(
    "--preview", is_flag=True, help="Preview what will happen but don't execute."
)
@click.option(
    "--skip-missing",
    is_flag=True,
    help=(
        "Skip repos that are not found in the source org, instead of failing. "
        "Useful after an error."
    ),
)
@click.option(
    '--no-prompt',
    is_flag=True,
    help="Don't ask for a confirmation before transferring the repos."
)
def migrate(src_org, dest_org, repo_list_file, preview, skip_missing, no_prompt):
    if preview:
        click.secho("In Preview Mode: No changes will be made!", italic=True)

    if src_org == dest_org:
        sys.exit("Fatal Error: Source and destination orgs must be different.")

    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        sys.exit("Fatal Error: Please set a GITHUB_TOKEN environment variable.")

    # Get the list of repos from our text file.
    repos_to_transfer = extract_repo_names(repo_list_file)
    click.echo(f"Read {len(repos_to_transfer)} repos from {repo_list_file.name}")

    api = GhApi(token=github_token)
    # Basic sanity check to make sure the repos we're transferring all actually exist.
    click.echo(f"Fetching the list of repos in source org {src_org}...")
    src_org_repos = {
        repo["name"]
        for repo in itertools.chain.from_iterable(
            paged(api.repos.list_for_org, src_org, per_page=100)
        )
    }
    missing_repos = [repo for repo in repos_to_transfer if repo not in src_org_repos]
    if missing_repos:
        if skip_missing:
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
            # If skip_missing isn't specified, treat missing repos as an error.
            # (Maybe they're trying to move things from the wrong org.)
            sys.exit(
                "Fatal Error: The following repos marked for transfer are not in "
                f"org {src_org}: {', '.join(missing_repos)}"
            )

    if not repos_to_transfer:
        sys.exit("No repos to transfer. Quitting.")

    if not no_prompt:
        click.echo()
        click.secho(
            f"The following {len(repos_to_transfer)} repositories will be moved from {src_org} to {dest_org}: ",
            nl=False,
            bold=True,
        )
        click.echo(", ".join(repos_to_transfer))
        click.echo()
        click.confirm('Proceed?', abort=True)

    with click.progressbar(
        repos_to_transfer,
        label=f"Transferring repositories from {src_org} to {dest_org}",
    ) as progress_bar:
        for repo in progress_bar:
            click.echo(f" {repo}")
            if not preview:
                api.repos.transfer(src_org, repo, dest_org)


def extract_repo_names(repo_list_file):
    comments_removed = [line.partition("#")[0] for line in repo_list_file]
    stripped = [line.strip() for line in comments_removed]
    empty_lines_removed = [line for line in stripped if line]
    return empty_lines_removed


if __name__ == "__main__":
    migrate()  # pylint: disable=no-value-for-parameter
