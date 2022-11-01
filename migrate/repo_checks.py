"""
Run checks Against Repos and correct them if they're missing something.

"""
import re
from itertools import chain
from pprint import pformat

import click
import requests
from fastcore.net import HTTP4xxClientError, HTTP5xxServerError, HTTP404NotFoundError
from ghapi.all import GhApi, paged

HAS_GHSA_SUFFIX = re.compile(".*?-ghsa-\w{4}-\w{4}-\w{4}$")


def is_security_private_fork(api, org, repo):
    """
    Check to see if a specific repo is a private security fork.
    """

    # Also make sure that it's a private repo.
    is_private = api.repos.get(org, repo).private

    return is_private and HAS_GHSA_SUFFIX.match(repo)


class Check:
    def __init__(self, api, org, repo):
        self.api = api
        self.org_name = org
        self.repo_name = repo

    def check(self):
        """
        Verify whether or not the check is failing.

        This should not change anything and should not have a side-effect.
        """

        raise NotImplementedError

    def fix(self):
        """
        Make an idempotent change to resolve the issue.
        """

        raise NotImplementedError

    def dry_run(self):
        """
        See what will happen without making any changes.
        """
        raise NotImplementedError


class RequiredCLACheck(Check):
    """
    This class validates the following:

    * Branch Protection is enabled on the default branch.
    * The CLA Check is a required check.

    If the check fails, the fix function can update the repo
    so that it has branch protection enabled with the "openedx/cla"
    check as a required check.
    """

    def __init__(self, api, org, repo):
        super().__init__(api, org, repo)

        self.cla_check = {"context": "openedx/cla", "app_id": -1}
        self.cla_team = "cla-checker"

        self.has_a_branch_protection_rule = False
        self.branch_protection_has_required_checks = False
        self.required_checks_has_cla_required = False
        self.team_setup_correctly = False

    def check(self):
        is_required_check = self._check_cla_is_required_check()
        repo_on_required_team = self._check_cla_team_has_write_access()

        value = is_required_check[0] and repo_on_required_team[0]
        reason = f"{is_required_check[1]} {repo_on_required_team[1]}"
        return (value, reason)

    def _check_cla_is_required_check(self):
        repo = self.api.repos.get(self.org_name, self.repo_name)
        default_branch = repo.default_branch
        # Branch protection rule might not exist.
        try:
            branch_protection = self.api.repos.get_branch_protection(
                self.org_name, self.repo_name, default_branch
            )
            self.has_a_branch_protection_rule = True
        except HTTP404NotFoundError as e:
            return (False, "No branch protection rule.")

        if "required_status_checks" not in branch_protection:
            return (False, "No required status checks in place.")
        self.branch_protection_has_required_checks = True

        # We don't need to check the `contexts` list because, github mirrors
        # all existing checks in `contexts` into the `checks` data.  The `contexts`
        # data is deprecated and will not be available in the future.
        contexts = [
            check["context"]
            for check in branch_protection.required_status_checks.checks
        ]
        if "openedx/cla" not in contexts:
            return (False, "CLA Check is not a required check.")
        self.required_checks_has_cla_required = True

        return (True, "Branch Protection with CLA Check is in Place.")

    def _check_cla_team_has_write_access(self):
        teams = chain.from_iterable(
            paged(
                self.api.repos.list_teams,
                self.org_name,
                self.repo_name,
                per_page=100,
            )
        )

        team_permissions = {team.slug: team.permission for team in teams}
        if self.cla_team not in team_permissions:
            return (False, f"'{self.cla_team}' team not listed on the repo.")
        # CLA Checker needs write access to push status but it doesn't need anything
        # higher than that.
        elif team_permissions[self.cla_team] != "push":
            return (
                False,
                f"'{self.cla_team}' team does not have the correct access. "
                f"Has {team_permissions[self.cla_team]} instead of push.",
            )
        else:
            self.team_setup_correctly = True
            return (True, f"'{self.cla_team}' team has 'push' access.")

    def dry_run(self):
        """
        Provide info on what would be done to make this check pass.
        """
        return self.fix(dry_run=True)

    def fix(self, dry_run=False):
        steps = []
        if not self.required_checks_has_cla_required:
            steps += self._fix_branch_protection(dry_run)

        if not self.team_setup_correctly:
            steps += self._fix_team_setup(dry_run)

        return steps

    def _fix_branch_protection(self, dry_run=False):
        try:
            steps = []

            # Short Circuit if there is nothing to do.
            if self.required_checks_has_cla_required:
                return steps

            repo = self.api.repos.get(self.org_name, self.repo_name)
            default_branch = repo.default_branch

            # While the API docs claim that "contexts" is a required part
            # of the put body, it is only required if "checks" is not supplied.
            required_status_checks = {
                "strict": False,
                "checks": [
                    self.cla_check,
                ],
            }

            if not self.has_a_branch_protection_rule:
                # The easy case where we don't already have branch protection setup.
                # Might not work actually because of the bug we found below.  We'll need
                # to test against github to verify.
                params = {
                    "owner": self.org_name,
                    "repo": self.repo_name,
                    "branch": default_branch,
                    "required_status_checks": required_status_checks,
                    "enforce_admins": None,
                    "required_pull_request_reviews": None,
                    "restrictions": None,
                }
                if not dry_run:
                    self._update_branch_protection(params)

                steps.append(
                    f"Added new branch protection with `openedx/cla` as a required check."
                )
                return steps

            # There's already a branch protection rule, so we need to make sure
            # not to clobber the existing checks or settings.
            params = self._get_update_params_from_get_branch_protection()
            steps.append(f"State Before Update: {pformat(dict(params))}")

            if not self.branch_protection_has_required_checks:
                # We need to add a check object to the params we get
                # since this branch protection rule has no required checks.
                steps.append(f"Adding a new required check.\n{required_status_checks}")
                params["required_status_checks"] = required_status_checks
            else:
                # There is already a set of required checks, we just need to
                # add our new check to the existing list.
                steps.append(
                    f"Adding `openedx/cla` as a new required check to existing branch protection."
                )
                params["required_status_checks"]["checks"].append(self.cla_check)

            if not self.required_checks_has_cla_required:
                # Have to do this because of a bug in GhAPI see
                # _update_branch_protection docstring for more details.
                steps.append(f"Update we're requesting: {pformat(dict(params))}")
                if not dry_run:
                    self._update_branch_protection(params)
                # self.api.repos.update_branch_protection(**params)
        except HTTP4xxClientError as e:
            # Print the steps before raising the existing exception so we have
            # some more context on what might have happened.
            click.echo("\n".join(steps))
            click.echo(e.fp.read().decode("utf-8"))
            raise
        except requests.HTTPError as e:
            # Print the steps before raising the existing exception so we have
            # some more context on what might have happened.
            click.echo("\n".join(steps))
            click.echo(pformat(e.response.json()))
            raise

        return steps

    def _fix_team_setup(self, dry_run=False):
        try:
            if not dry_run:
                self.api.teams.add_or_update_repo_permissions_in_org(
                    self.org_name,
                    self.cla_team,
                    self.org_name,
                    self.repo_name,
                    "push",
                )
            return [f"Added push access for {self.cla_team} to {self.repo_name}."]
        except HTTP4xxClientError as e:
            click.echo(e.fp.read().decode("utf-8"))
            raise

    def _update_branch_protection(self, params):
        """
        Need to do this ourselves because of a bug in GhAPI that ignores
        `None` parameters and doesn't pass them through to the API.

        - https://github.com/fastai/ghapi/issues/81
        - https://github.com/fastai/ghapi/pull/91
        """
        params = dict(params)
        headers = self.api.headers
        url = (
            "https://api.github.com"
            + self.api.repos.update_branch_protection.path.format(**params)
        )
        resp = requests.put(url, headers=headers, json=params)

        resp.raise_for_status()

    def _get_update_params_from_get_branch_protection(self):
        """
        Get the params needed to do an update operation that would produce
        the same branch protection as doing a get on this repo.

        We'll need this in cases where there are already some branch protection
        rules on the default branch and we want to update only some it without
        resetting the rest of it.
        """

        # TODO: Could use Glom here in the future, but didn't need it.
        repo = self.api.repos.get(self.org_name, self.repo_name)
        default_branch = repo.default_branch
        bp = self.api.repos.get_branch_protection(
            self.org_name, self.repo_name, default_branch
        )

        required_checks = None
        if "required_status_checks" in bp:
            # While the API docs claim that "contexts" is a required part
            # of the put body, it is only required if "checks" is not supplied.
            # The GET endpoint provides the curent set of required checks in both
            # format. So we only use the new "checks" format in our PUT params.
            required_checks = {
                "strict": bp.required_status_checks.strict,
                "checks": list(bp.required_status_checks.checks),
            }

        required_pr_reviews = None
        if "required_pull_request_reviews" in bp:
            required_pr_reviews = {
                "dismiss_stale_reviews": bp.required_pull_request_reviews.dismiss_stale_reviews,
                "require_code_owner_reviews": bp.required_pull_request_reviews.require_code_owner_reviews,
                "required_approving_review_count": bp.required_pull_request_reviews.required_approving_review_count,
            }

        restrictions = None
        if "restrictions" in bp:
            restrictions = {
                "users": [user.login for user in bp.restrictions.users],
                "teams": [team.slug for team in bp.restrictions.teams],
                "apps": [app.slug for app in bp.restrictions.apps],
            }

        params = {
            "owner": self.org_name,
            "repo": self.repo_name,
            "branch": default_branch,
            "required_status_checks": required_checks,
            "enforce_admins": True if bp.enforce_admins.enabled else None,
            "required_pull_request_reviews": required_pr_reviews,
            "restrictions": restrictions,
        }

        return params


CHECKS = [RequiredCLACheck]


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
    help="The github org that you wish check.",
)
@click.option(
    "--dry-run/--no-dry-run",
    "-n",
    default=True,
    is_flag=True,
    help="Show what changes would be made without making them.",
)
def main(org, dry_run, github_token):
    api = GhApi()
    repos = [
        repo.name
        for repo in chain.from_iterable(
            paged(api.repos.list_for_org, org, per_page=100)
        )
    ]

    for repo in repos:
        if is_security_private_fork(api, org, repo):
            continue

        click.secho(f"{repo}: ")
        for CheckType in CHECKS:
            check = CheckType(api, org, repo)

            result = check.check()
            if result[0]:
                color = "green"
            else:
                color = "red"

            click.secho(f"\t{result[1]}", fg=color)

            if dry_run:
                steps = check.dry_run()
                steps_color = "yellow"
            else:
                steps = check.fix()
                steps_color = "green"

            if steps:
                click.secho("\tSteps:\n\t\t", fg=steps_color, nl=False)
                click.secho(
                    "\n\t\t".join([step.replace("\n", "\n\t\t") for step in steps])
                )


if __name__ == "__main__":
    main()