"""
Run checks Against Repos and correct them if they're missing something.

Needs a token with the following scopes:

    - admin:org
    - repo
    - user
    - workflow
"""
import re
import textwrap
from base64 import standard_b64decode, standard_b64encode
from functools import cache
from itertools import chain
from pprint import pformat

import click
import requests
from fastcore.net import (
    HTTP4xxClientError,
    HTTP5xxServerError,
    HTTP404NotFoundError,
    HTTP409ConflictError,
)
from ghapi.all import GhApi, paged

HAS_GHSA_SUFFIX = re.compile(r".*?-ghsa-\w{4}-\w{4}-\w{4}$")


def is_security_private_fork(api, org, repo):
    """
    Check to see if a specific repo is a private security fork.
    """

    # Also make sure that it's a private repo.
    is_private = api.repos.get(org, repo).private

    return is_private and HAS_GHSA_SUFFIX.match(repo)


def is_public(api, org, repo):
    """
    Check to see if a specific repo is public.
    """

    is_private = api.repos.get(org, repo).private

    return not is_private


def is_empty(api, org, repo):
    """
    Check to see if a specific repo is empty and has no commits yet.
    """
    default_branch = api.repos.get(org, repo).default_branch

    try:
        default_branch_ref = api.git.get_ref(
            org,
            repo,
            f"heads/{default_branch}",
        )
    except HTTP409ConflictError as e:
        if "Git Repository is empty." in e.fp.read().decode():
            return True
        raise
    except Exception as e:
        breakpoint()
        raise

    return False


@cache
def get_github_file_contents(api, org, repo, path, ref):
    """
    A caching proxy for the get repository content api endpoint.

    It returns the content of the file as a string.
    """
    return api.repos.get_content(org, repo, path, ref).content


class Check:
    def __init__(self, api, org, repo):
        self.api = api
        self.org_name = org
        self.repo_name = repo

    def is_relevant(self):
        """
        Checks to see if the given check is relevant to run on the
        given repo.

        This is independent of whether or not the check passes on this repo
        and should be run before trying to check the repo.
        """

        raise NotImplementedError

    def check(self) -> (bool, str):
        """
        Verify whether or not the check is failing.

        This should not change anything and should not have a side-effect.

        The string in the return tuple should be a human readable reason
        that the check failed.
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


class EnsureWorkflowTemplates(Check):
    """
    There are certain github action workflows that we to exist on all
    repos exactly as they are defined in the `.github` repo in the org.

    Check to see if they're in a repo and if not, make a pull request
    to add them to the repository.
    """

    def __init__(self, api: GhApi, org: str, repo: str):
        super().__init__(api, org, repo)

        self.workflow_templates = [
            "self-assign-issue.yml",
            "add-depr-ticket-to-depr-board.yml",
            "commitlint.yml",
            "add-remove-label-on-comment.yml",
        ]

        self.branch_name = "repo_checks/ensure_workflows"

        self.files_to_create = []
        self.files_to_update = []
        self.dot_github_template_contents = {}

    def is_relevant(self):
        return (
            is_public(self.api, self.org_name, self.repo_name)
            and not is_empty(self.api, self.org_name, self.repo_name)
        )

    def check(self):
        """
        See if our workflow templates are in the repo and have the same content
        as the default templates in the `.github` repo.
        """
        # Get the current default branch.
        repo = self.api.repos.get(self.org_name, self.repo_name)
        default_branch = repo.default_branch

        files_that_differ, files_that_are_missing = self._check_branch(default_branch)
        # Return False and save the list of files that need to be updated.
        if files_that_differ or files_that_are_missing:
            self.files_to_create = files_that_are_missing
            self.files_to_update = files_that_differ
            return (
                False,
                f"Some workflows in this repo don't match the template.\n\t\t{files_that_differ=}\n\t\t{files_that_are_missing=}",
            )

        return (
            True,
            "All desired workflows are in sync with what's in the .github repo.",
        )

    def _check_branch(self, branch_name):
        """
        Check the contents the listed workflow files on a branch against the
        default content in the .github folder.
        """
        dot_github_default_branch = self.api.repos.get(
            self.org_name, ".github"
        ).default_branch
        # Get the content of the .github files, maybe this should be a memoized
        # function since we'll want to get the same .github content from all
        # the repos.
        for file in self.workflow_templates:
            file_path = f"workflow-templates/{file}"
            try:
                self.dot_github_template_contents[file] = get_github_file_contents(
                    self.api,
                    self.org_name,
                    ".github",
                    file_path,
                    dot_github_default_branch,
                )
            except HTTP4xxClientError as e:
                click.echo(
                    f"File: https://github.com/{org_name}/.github/blob/{dot_github_default_branch}/{file_path}"
                )
                click.echo(e.fp.read().decode("utf-8"))
                raise

        # Get the content of the repo specific file.
        repo_contents = {}
        files_that_are_missing = []
        for file in self.workflow_templates:
            file_path = f".github/workflows/{file}"
            try:
                repo_contents[file] = get_github_file_contents(
                    self.api,
                    self.org_name,
                    self.repo_name,
                    file_path,
                    branch_name,
                )
            except HTTP4xxClientError as e:
                if e.status == 404:
                    files_that_are_missing.append(file)

        # Compare the two.
        files_that_differ = []
        for file in self.workflow_templates:
            if (
                file not in files_that_are_missing
                and self.dot_github_template_contents[file] != repo_contents[file]
            ):
                files_that_differ.append(file)

        return (files_that_differ, files_that_are_missing)

    def dry_run(self):
        return self.fix(dry_run=True)

    def fix(self, dry_run=False):
        """
        Always use the same branch name and update the contents if necessary.
        """

        steps = []
        # Check to see if the update branch already exists.
        branch_exists = True
        try:
            self.api.git.get_ref(
                self.org_name, self.repo_name, f"heads/{self.branch_name}"
            )
        except HTTP4xxClientError as e:
            if e.status == 404:
                branch_exists = False
            else:
                raise  # For any other unexpected errors.

        # Get the hash of the default branch.
        repo = self.api.repos.get(self.org_name, self.repo_name)
        default_branch = repo.default_branch
        default_branch_sha = self.api.git.get_ref(
            self.org_name,
            self.repo_name,
            f"heads/{default_branch}",
        ).object.sha

        if branch_exists:
            steps.append("Workflow branch already exists.  Updating branch.")

            if not dry_run:
                # Force-push the branch to the lastest sha of the default branch.
                self.api.git.update_ref(
                    self.org_name,
                    self.repo_name,
                    f"heads/{self.branch_name}",
                    default_branch_sha,
                    force=True,
                )

        else:  # The branch does not exist
            steps.append(f"Branch does not exist. Creating '{self.branch_name}'.")
            if not dry_run:
                self.api.git.create_ref(
                    self.org_name,
                    self.repo_name,
                    # The create api needs the `refs/` prefix while the get api doesn't,
                    # be sure to check the API reference before adding calls to other
                    # parts of the GitHub `git/refs` REST api.
                    # https://docs.github.com/en/rest/git/refs?apiVersion=2022-11-28
                    f"refs/heads/{self.branch_name}",
                    default_branch_sha,
                )

        steps.append(f"Updating workflow files on '{self.branch_name}'.")
        commit_message_template = textwrap.dedent(
            """
            build: {creating_or_updating} a missing workflow file `{workflow}`.

            The {path_in_repo} workflow is missing or needs an update to stay in
            sync with the current standard for this workflow as defined in the
            `.github` repo of the `{org_name}` GitHub org.
            """
        )

        for workflow in self.files_to_create + self.files_to_update:
            if workflow in self.files_to_create:
                creating_or_updating = "Creating"
            else:
                creating_or_updating = "Updating"

            path_in_repo = f".github/workflows/{workflow}"
            commit_message = commit_message_template.format(
                creating_or_updating=creating_or_updating,
                path_in_repo=path_in_repo,
                workflow=workflow,
                org_name=self.org_name,
            )
            file_content = self.dot_github_template_contents[workflow]

            steps.append(f"{creating_or_updating} {path_in_repo}")
            if not dry_run:
                # We need the sha to update an existing file.
                if workflow in self.files_to_create:
                    current_file_sha = None
                else:
                    current_file_sha = self.api.repos.get_content(
                        self.org_name,
                        self.repo_name,
                        path_in_repo,
                        self.branch_name,
                    ).sha

                self.api.repos.create_or_update_file_contents(
                    owner=self.org_name,
                    repo=self.repo_name,
                    path=path_in_repo,
                    message=commit_message,
                    content=file_content,
                    sha=current_file_sha,
                    branch=self.branch_name,
                )

        # Check to see if a PR exists
        prs = chain.from_iterable(
            paged(
                self.api.pulls.list,
                owner=self.org_name,
                repo=self.repo_name,
                head=self.branch_name,
                per_page=100,
            )
        )

        prs = list([pr for pr in prs if pr.head.ref == self.branch_name])

        if prs:
            steps.append(f"PR already exists: {prs[0].html_url}")
        else:
            # If not, create a new PR
            steps.append("No PR exists, creating a PR.")
            if not dry_run:
                pr = self.api.pulls.create(
                    owner=self.org_name,
                    repo=self.repo_name,
                    title="Update standard workflow files.",
                    head=self.branch_name,
                    base=default_branch,
                    body="",
                    maintainer_can_modify=True,
                )
                steps.append(f"New PR: {pr.html_url}")

        return steps


class EnsureLabels(Check):
    """
    All repos in the org should have certain labels.
    """

    def __init__(self, api: GhApi, org: str, repo: str):
        super().__init__(api, org, repo)
        # A list of labels mapped to their hex colors
        # so that they are the same color in all the repos.
        # Relevant API Docs: https://docs.github.com/en/rest/issues/labels#create-a-label
        # https://www.htmlcolor-picker.com/
        self.labels = {
            ":hammer_and_wrench: maintenance": "169509",
            "waiting on author": "bfd6f6",
            "inactive": "ff950a",
            "closed-inactivity": "dbcd00",
            "needs test run": "f5424b",
            "good first issue :tada:": "43dd35",
        }

    def is_relevant(self):
        return not is_security_private_fork(self.api, self.org_name, self.repo_name)

    def check(self):
        """
        See if our labels exist.
        """
        labels = chain.from_iterable(
            paged(
                self.api.issues.list_labels_for_repo,
                self.org_name,
                self.repo_name,
                per_page=100,
            )
        )

        existing_labels = {
            self._simplify_label(label.name): {"color": label.color, "name": label.name}
            for label in labels
        }
        self.missing_labels = []
        self.labels_that_need_updates = []
        # [
        #     {
        #         "current_label": "<current label name>",
        #         "new_label": "<new_label_name>",
        #         "color": "<new_label_color>",
        #     }
        # ]

        for new_label, new_color in self.labels.items():
            simple_new_label = self._simplify_label(new_label)
            if simple_new_label in existing_labels:
                # We need to potentially update the label if the name or color have changed.
                current_label = existing_labels[simple_new_label]
                if (
                    current_label["name"] != new_label
                    or current_label["color"] != new_color
                ):
                    self.labels_that_need_updates.append(
                        {
                            "current_label": existing_labels[simple_new_label]["name"],
                            "new_label": new_label,
                            "new_color": new_color,
                        }
                    )
            else:
                # We need to create the label as it doesn't already exist.
                self.missing_labels.append(new_label)

        if self.missing_labels or self.labels_that_need_updates:
            return (
                False,
                f"Labels need updating. {self.missing_labels=}  {self.labels_that_need_updates=}",
            )
        return (True, "All desired labels exist with the right color.")

    def dry_run(self):
        return self.fix(dry_run=True)

    def fix(self, dry_run=False):
        steps = []

        # Create missing labels
        for label in self.missing_labels:
            if not dry_run:
                try:
                    self.api.issues.create_label(
                        self.org_name,
                        self.repo_name,
                        label,
                        self.labels[label],
                    )
                except HTTP4xxClientError as e:
                    click.echo(e.fp.read().decode("utf-8"))
                    raise
            steps.append(f"Created {label=}.")

        # Update incorrectly colored labels
        for label in self.labels_that_need_updates:
            if not dry_run:
                try:
                    self.api.issues.update_label(
                        self.org_name,
                        self.repo_name,
                        name=label["current_label"],
                        color=label["new_color"],
                        new_name=label["new_label"],
                    )
                except HTTP4xxClientError as e:
                    click.echo(e.fp.read().decode("utf-8"))
                    raise
            steps.append(f"Updated color for {label=}")

        return steps

    def _simplify_label(self, label: str):
        special_content = re.compile(r"(:\S+:|-|_|'|\"|\.|\!|\s)")

        simplified_label = special_content.sub("", label).strip().lower()
        return simplified_label


class RequireTeamPermission(Check):
    """
    Require that a team has a certain level of access to a repository.

    To use this class as a check, create a subclass that specifies a particular
    team and permission level, such as RequireTriageTeamAccess below.
    """

    def __init__(self, api: GhApi, org: str, repo: str, team: str, permission: str):
        """
        Valid permission strings are defined in the Github REST API docs:

        https://docs.github.com/en/rest/teams/teams#add-or-update-team-repository-permissions

        They include 'pull', 'triage', 'push', 'maintain', and 'admin'.
        """
        super().__init__(api, org, repo)
        self.team = team
        self.permission = permission

        self.team_setup_correctly = False

    def check(self):
        teams = chain.from_iterable(
            paged(
                self.api.repos.list_teams,
                self.org_name,
                self.repo_name,
                per_page=100,
            )
        )

        team_permissions = {team.slug: team.permission for team in teams}
        if self.team not in team_permissions:
            return (False, f"'{self.team}' team not listed on the repo.")
        # Check to see if the team has the correct permission.
        # More and less acess are both considered incorrect.
        elif team_permissions[self.team] != self.permission:
            return (
                False,
                f"'{self.team}' team does not have the correct access. "
                f"Has {team_permissions[self.team]} instead of {self.permission}.",
            )
        else:
            self.team_setup_correctly = True
            return (True, f"'{self.team}' team has '{self.permission}' access.")

    def dry_run(self):
        """
        Provide info on what would be done to make this check pass.
        """
        return self.fix(dry_run=True)

    def fix(self, dry_run=False):
        if self.team_setup_correctly:
            return []

        try:
            if not dry_run:
                self.api.teams.add_or_update_repo_permissions_in_org(
                    self.org_name,
                    self.team,
                    self.org_name,
                    self.repo_name,
                    self.permission,
                )
            return [
                f"Added {self.permission} access for {self.team} to {self.repo_name}."
            ]
        except HTTP4xxClientError as e:
            click.echo(e.fp.read().decode("utf-8"))
            raise


class RequireTriageTeamAccess(RequireTeamPermission):
    """
    The Core Contributor Triage Team needs to be able to triage
    issues in all repos in the Open edX Platform.

    The check function will tell us if the team has the correct level of access
    and the fix function will make it so if it does not.
    """

    def __init__(self, api, org, repo):
        team = "community-pr-triage-managers"
        permission = "triage"
        super().__init__(api, org, repo, team, permission)

    def is_relevant(self):
        # Need to be a public repo.
        return is_public(self.api, self.org_name, self.repo_name)


class RequireProductManagersAccess(RequireTeamPermission):
    """
    The Open edX Product Managers team needs to be able to triage issue
    in all repos of the Open edX Platform.
    """

    def __init__(self, api, org, repo):
        team = "open-edx-product-managers"
        permission = "triage"
        super().__init__(api, org, repo, team, permission)

    def is_relevant(self):
        # Need to be a public repo.
        return is_public(self.api, self.org_name, self.repo_name)


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
        self.cla_team_permission = "push"

        self.team_check = RequireTeamPermission(
            api,
            org,
            repo,
            self.cla_team,
            self.cla_team_permission,
        )

        self.has_a_branch_protection_rule = False
        self.branch_protection_has_required_checks = False
        self.required_checks_has_cla_required = False
        self.team_setup_correctly = False

    def is_relevant(self):
        return not is_security_private_fork(self.api, self.org_name, self.repo_name)

    def check(self):
        is_required_check = self._check_cla_is_required_check()
        repo_on_required_team = self.team_check.check()

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

    def dry_run(self):
        """
        Provide info on what would be done to make this check pass.
        """
        return self.fix(dry_run=True)

    def fix(self, dry_run=False):
        steps = []
        if not self.required_checks_has_cla_required:
            steps += self._fix_branch_protection(dry_run)

        if not self.team_check.team_setup_correctly:
            steps += self.team_check.fix(dry_run)

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

                if is_empty(self.api, self.org_name, self.repo_name):
                    steps.append(
                        "Repo has no branches, can't add branch protection rule yet."
                    )
                else:
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


CHECKS = [
    RequiredCLACheck,
    RequireTriageTeamAccess,
    RequireProductManagersAccess,
    EnsureLabels,
    EnsureWorkflowTemplates,
]


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
@click.option(
    "--target",
    "-t",
    multiple=True,
)
def main(org, dry_run, github_token, target):
    api = GhApi()
    if target:
        repos = target
    else:
        repos = [
            repo.name
            for repo in chain.from_iterable(
                paged(
                    api.repos.list_for_org,
                    org,
                    sort="created",
                    direction="desc",
                    per_page=100,
                )
            )
        ]
    if dry_run:
        click.secho("DRY RUN MODE: No Actual Changes Being Made", fg="yellow")

    for repo in repos:
        click.secho(f"{repo}: ")
        for CheckType in CHECKS:
            check = CheckType(api, org, repo)

            if check.is_relevant():
                result = check.check()
                if result[0]:
                    color = "green"
                else:
                    color = "red"

                click.secho(f"\t{result[1]}", fg=color)

                if dry_run:
                    try:
                        steps = check.dry_run()
                        steps_color = "yellow"
                    except HTTP4xxClientError as e:
                        click.echo(e.fp.read().decode("utf-8"))
                        raise
                else:
                    try:
                        steps = check.fix()
                        steps_color = "green"
                    except HTTP4xxClientError as e:
                        click.echo(e.fp.read().decode("utf-8"))
                        raise

                if steps:
                    click.secho("\tSteps:\n\t\t", fg=steps_color, nl=False)
                    click.secho(
                        "\n\t\t".join([step.replace("\n", "\n\t\t") for step in steps])
                    )
            else:
                click.secho(f"Skipping {CheckType} as it is not relevant on this repo.")


if __name__ == "__main__":
    main()
