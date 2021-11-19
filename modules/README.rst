
modules
-------

A *module* is a re-usable Terraform component. Conceptually, each module can be thought of as a function: it takes arguments (*variables*) and returns results (*resources* and *outputs*).

Each sub-directory within this directory is a module representing an Open edX GitHub concept:

* A **repo** generates zero or one GitHub repositories with some standard settings.
* A **user** represents a GitHub user that is a committer to the Open edX project, and may or may not generate a membership in the ``openedx`` GitHub organization.
* A **role** consumes users and repositories, and generates resources to grant a level of permission to each user on each repository.
