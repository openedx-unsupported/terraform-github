terraform-github
----------------

This repository contains scripts to manage the migration of many ``edx`` and ``edx-solutions`` repositories to the ``openedx`` GitHub organization.


How it works
============

WIP

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

State of this repository
========================

We are currently in a transitory phase: the upstream repositories comprising Open edX project are being pulled together from three different GitHub organizations (``edx``, ``edx-solutions``, and ``openedx``) into just one (``openedx``). Furthermore, we are considering moving the ``openedx`` GitHub organization from being completely managed from the GitHub settings UI to being completely managed via Terraform. For now, expect some confusion and inconsistency between this code and reality.


Usage
=====

WIP

Formatting
**********

Terraform code can be auto-formatted without any additional setup::

  terraform fmt  # Formats the current directory.
  make format    # Formats all Terraform in this repository.

Credentials
***********

GitHub credentials with owner-level access to the ``openedx`` organization are required to apply the Terraform. Generate a personal access token and export it as::

  export GITHUB_TOKEN=...


Initializing, validating, planning, applying
********************************************

WIP
