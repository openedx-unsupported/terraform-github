"""
Used by the Python scripts in this repo.
"""

from typing import NewType, Optional

RepoAccessLevel = NewType("RepoAccessLevel", int)
Username = NewType("Username", str)
TeamSlug = NewType("TeamSlug", str)  # the mention-able "name" of the team
RepoName = NewType("RepoName", str)  # no 'org/' prefix

REPO_ADMIN = RepoAccessLevel(4)
REPO_MAINTAIN = RepoAccessLevel(3)
REPO_WRITE = RepoAccessLevel(2)
REPO_READ = RepoAccessLevel(1)
REPO_NONE = RepoAccessLevel(0)


def access_level_to_string(access_level: RepoAccessLevel) -> Optional[str]:
    """
    Convert from integer access level to GH-understood string representation,
    returning 'None' for no-access.
    """
    assert (
        REPO_NONE <= access_level <= REPO_ADMIN
    ), f"invalid RepoAccessLevel int value: {access_level}"
    return {
        REPO_ADMIN: "admin",
        REPO_MAINTAIN: "maintain",
        REPO_WRITE: "push",
        REPO_READ: "pull",
        REPO_NONE: None,
    }[access_level]
