from itertools import chain
from textwrap import dedent

import click
from cache_to_disk import cache_to_disk, delete_disk_caches_for_function
from ghapi.all import GhApi, paged

PUBLIC_REPO_MODULE_TEMPLATE = dedent(
    """
    module "{module_name}" {{
        source = "./modules/repo"
        name = "{repo_name}"
    }}

    """
)

NON_PUBLIC_REPO_MODULE_TEMPLATE = dedent(
    """
    module "{module_name}" {{
        source = "./modules/repo"
        name = "{repo_name}"
        visibility = "{visibility}"
    }}

    """
)


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
@click.option(
    "--refresh-cache",
    help="Refresh cache of github data before running.",
    default=False,
    is_flag=True,
)
@click.option(
    "--github-token",
    envvar="GITHUB_TOKEN",
    required=True,
    help="A github personal access token.",
)
@click.option(
    "--public-repos-file",
    default="../repos.tf",
    type=click.File("w"),
    help="The file to write the github repo modules to.",
)
@click.option(
    "--private-repos-file",
    default="../private.tf",
    type=click.File("w"),
    help="The file to write the github repo modules to.",
)
@click.option(
    "--import-commands-file",
    default="../import.sh",
    type=click.File("w"),
    help="The file provides the terraform import commands to import the repos.",
)
@click.command()
def main(
    org,
    dry_run,
    refresh_cache,
    github_token,
    public_repos_file,
    private_repos_file,
    import_commands_file,
):
    api = GhApi()
    repos = chain.from_iterable(paged(api.repos.list_for_org, org, per_page=100))

    for repo in repos:
        if repo.visibility == "public":
            repos_file = public_repos_file
            template = PUBLIC_REPO_MODULE_TEMPLATE
        else:
            repos_file = private_repos_file
            template = NON_PUBLIC_REPO_MODULE_TEMPLATE

        module_name = repo.name.replace("-", "_").replace(".", "_")
        repos_file.write(
            template.format(
                module_name=module_name, repo_name=repo.name, visibility=repo.visibility
            )
        )

        import_commands_file.write(
            f"terraform import 'module.{module_name}.github_repository.repo' {repo.name}\n"
        )


if __name__ == "__main__":
    main()
