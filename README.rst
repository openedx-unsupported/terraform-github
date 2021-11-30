terraform-github
----------------

This repository contains:

* Terraform plan(s) to manage users, repositories, teams, and other entities within the ``openedx`` GitHub organization, and
* associated scripts for generating and managing said Terraform.

.. image:: https://user-images.githubusercontent.com/3628148/143911459-6b269a21-6c7b-4a49-80ea-c1b9568af9da.png
  :alt: Logos of GitHub, Terraform and Open edX


How it works
============

`Terraform <https://www.terraform.io/>`_ is a declarative langugage for configuring infrasturcture as code. Infrastructure is modeled as a collection of *resources* which can be managed.

The `GitHub Terraform provider <https://registry.terraform.io/providers/integrations/github/latest/docs>`_ exposes resources that correspond to entities in GitHub's official API, such as ``github_repository_collaborator`` and ``github_branch_protection``. This repository defines and uses Terraform modules that generate ``github_`` resources. The (understood) *state* of all of these resources is saved in an S3 bucket.

By running ``terraform plan``, a diff between the Terraform code (in this repository) and the Terraform state (in S3) is reported. This diff is called a *plan*. By running ``terraform apply``, the plan is applied to the Terraform state and changes to the state are applied to reality via the GitHub API. It is worth noting that the Terraform state is not always a total or perfect reflection of the underlying resources in reality; while this can cause toil and confusion in the long run, it is expected when transitioning resources into Terraform management.

Repository structure
====================

+----------------------------+--------------------------------------------------------------------------------------------------------------------------------+
| Path                       | Use                                                                                                                            |
+============================+================================================================================================================================+
| ./modules/                 | Re-usable Terraform structures ('role', 'repo', etc.). See the `modules README <./modules>`_.                                  |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------+
| ./migrate/                 | Temporary scripts and data for bringing edx, edx-solutions, and openedx repos into Terraform management under the openedx org. |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------+
| ./main.tf                  | Top-level Terraform configuration.                                                                                             |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------+
| ./repos_{org}.tf           | Repositories, as imported from {org}. Will eventually be re-sorted by purpose instead of original organization.                |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------+
| ./users_{org}.tf           | Members and collaborators, as imported from {org}. Will eventually be re-sorted by firm (TCRIL, RaccoonGang, edX, etc.).       |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------+
| ./roles_{org}.tf           | Roles (mapping users to repo permissions, ie pseudo-teams) as built from {org}. Subject to refactoring and pruning.            |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------+
| ./env                      | Utility script for sourcing (git-ignored) secrets.                                                                             |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------+
| ./.terraform.lock.hcl      | Lockfile for precise versions of installed Terraform providers. Essentially package-lock.json but for Terraform.               |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------+

State of this repository
========================

We are currently in a transitory phase: the upstream repositories comprising Open edX project are being pulled together from three different GitHub organizations (``edx``, ``edx-solutions``, and ``openedx``) into just one (``openedx``). Furthermore, the ``openedx`` GitHub organization is moving from being completely managed from the GitHub settings UI to being completely managed via Terraform. For now, expect some confusion and inconsistency between this code and reality.

Things that *are* currently reflected in Terraform:

* Public repositories.
* Push, maintainer, and admin permissions on public repositories (assigned via instances of the *role* module).
* Repositories and permissions thereof that are currently within ``edx`` and ``edx-solutions``, but will soon be pulled into ``openedx``. These repositories are marked in Terraform by the *phony* attribute.

Things that are *not* currently reflected in Terraform:

* Most repository-level setttings (eg, branch protection rules).
* Organization-level settings.
* Organization member and owner relationships.
* Private repositories.
* Public and private project boards.
* Teams.

Usage
=====

Soon, a GitHub Action will be used to plan and apply all pull requests to this repository. For now, it must be done manually. Installation of Terraform >= 1.01 is required.

Formatting
**********

Terraform code can be auto-formatted without any additional setup::

  terraform fmt  # Formats the current directory.
  make format    # Formats all Terraform in this repository.

Credentials
***********

AWS S3 credentials are required to initialize, validate, and plan the Terraform. Attain read/write access to the ``openedx-terraform-github-state`` S3 bucket. Generate a AWS key ID/secret pair, and export them as::

  export AWS_ACCESS_KEY_ID=...
  export AWS_SECRET_ACCESS_KEY=...

GitHub credentials with owner-level access to the ``openedx`` organization are required to apply the Terraform. Generate a personal access token and export it as::

  export GITHUB_TOKEN=...


Initializing, validating, planning, applying
********************************************

Initialize Terraform::

  terraform init

Lint and type-check the Terraform::

  terraform validate

Generate a Terraform plan::

  terraform plan

And apply the plan to state and reality (DANGEROUS!)::

  terraform apply
