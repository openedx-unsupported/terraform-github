
variable "admin_repos" {
  type        = list(object({ name = string, phony = bool }))
  description = "GitHub repositories to which user has administrator (ie, total) access."
  default     = []
}

variable "maintain_repos" {
  type        = list(object({ name = string, phony = bool }))
  description = "GitHub repositories to which user has maintainer (ie, write+configure) access"
  default     = []
}

variable "push_repos" {
  type        = list(object({ name = string, phony = bool }))
  description = "GitHub repositories to which user has push (ie, write) access."
  default     = []
}

variable "pull_repos" {
  type        = list(object({ name = string, phony = bool }))
  description = "Private GitHub repositories to which user has pull (ie, read) access."
  default     = []
}

variable "users" {
  type        = list(object({ username = string }))
  description = "Users to which role will be granted."
}

locals {

  // Build a flat list of (username, repository, permission) objects.
  // Make sure to filter out permissions that act upon phony repositories.
  admin_user_repo_permissions = flatten([
    for user in var.users : [
      for repo in var.admin_repos : {
        username   = user.username
        repository = repo.name
        permission = "admin"
      }
      if !repo.phony
    ]
  ])
  maintain_user_repo_permissions = flatten([
    for user in var.users : [
      for repo in var.maintain_repos : {
        username   = user.username
        repository = repo.name
        permission = "maintain"
      }
      if !repo.phony
    ]
  ])
  push_user_repo_permissions = flatten([
    for user in var.users : [
      for repo in var.push_repos : {
        username   = user.username
        repository = repo.name
        permission = "push"
      }
      if !repo.phony
    ]
  ])
  pull_user_repo_permissions = flatten([
    for user in var.users : [
      for repo in var.pull_repos : {
        username   = user.username
        repository = repo.name
        permission = "pull"
      }
      if !repo.phony
    ]
  ])
  all_user_repo_permissions = concat(
    local.admin_user_repo_permissions,
    local.maintain_user_repo_permissions,
    local.push_user_repo_permissions,
    local.pull_user_repo_permissions,
  )

  // A map from a "$username:$repository" string to its corresponding
  // user_repository_permissions object.
  // This enables us to use `for_each` below.
  all_user_repo_permissions_map = {
    for urp in local.all_user_repo_permissions :
    "${urp.username}:${urp.repository}" => urp
  }
}

resource "github_repository_collaborator" "this" {
  for_each = local.all_user_repo_permissions_map

  username                    = each.value.username
  repository                  = each.value.repository
  permission                  = each.value.permission
  permission_diff_suppression = false
}
