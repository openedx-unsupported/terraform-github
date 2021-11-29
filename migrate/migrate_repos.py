import itertools
import sys
import time

import click
from ghapi.all import GhApi, paged

@click.command()
@click.option(
    '--preview',
    is_flag=True,
    help="Preview what will happen but don't execute."
)
@click.argument('src_org')
@click.argument('dest_org')
@click.argument('repo_list_file', type=click.File('r'))
def migrate(preview, src_org, dest_org, repo_list_file):
    if preview:
        click.echo("In Preview Mode: No changes will be made!")

    if src_org == dest_org:
        sys.exit("Fatal Error: Source and destination orgs must be different.")

    # Get the list of repos from our text file.
    repos_to_transfer = [
        repo_name.strip() for repo_name in repo_list_file if repo_name.strip()
    ]

    api = GhApi()
    # Basic sanity check to make sure the repos we're transferring all actually exist.
    src_org_repos = {
        repo['name']
        for repo
        in itertools.chain.from_iterable(paged(api.repos.list_for_org, src_org, per_page=100))
    }
    missing_repos = [repo for repo in repos_to_transfer if repo not in src_org_repos]
    if missing_repos:
        sys.exit(
            "Fatal Error: The following repos marked for transfer are not in "
            f"org {src_org}: {', '.join(missing_repos)}"
        )

    with click.progressbar(repos_to_transfer,
                           label=f"Transferring repositories from {src_org} to {dest_org}") as bar:
        for repo in bar:
            click.echo(f" {repo}")
            if not preview:
                1/0  # Yes, I'm paranoid.
                api.repos.transfer(src_org, repo, dest_org)

if __name__ == '__main__':
    migrate()
