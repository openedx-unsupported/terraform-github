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
| ./migrate/                 | Temporary scripts and data for migrating edx and edx-solutions repos to the openedx organization.                              |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------+
| ./modules/                 | Re-usable Terraform structures ('role', 'repo', etc.). See the `modules README <./modules>`_. **Not used currently.**          |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------+
| ./main.tf                  | Top-level Terraform configuration. **Not used currently.**                                                                     |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------+

State of this repository
========================

We are currently in a transitory phase: the upstream repositories comprising Open edX project are being pulled together from three different GitHub organizations (``edx``, ``edx-solutions``, and ``openedx``) into just one (``openedx``). Furthermore: although we hope to eventually move the ``openedx`` GitHub organization entirely under Terraform management, we are currently prioritizing this below the repository migration, so all Terraform in this repository is aspirational.


Usage
=====

Credentials
***********

GitHub credentials with owner-level access to the ``openedx`` organization are required to run migration scripts or apply Terraform. Generate a personal access token and export it as::

  export GITHUB_TOKEN=...


Migration scripts
*****************

You can run any the Python script under ``migrate/`` without arguments in order to see a usage guide.


Formatting Terraform
********************

Terraform code can be auto-formatted without any additional setup::

  terraform fmt  # Formats the current directory.
  make format    # Formats all Terraform in this repository.


Initializing, validating, planning, applying Terraform
******************************************************

WIP
