
variable "name" {
  type        = string
  description = "Name of the GitHub repository"
}

variable "visibility" {
  type        = string
  description = "Repository visibility ('public', 'private', or 'secret'. Defaults 'public')."
  default     = "public"
}

resource "github_repository" "repo" {
  name       = var.name
  visibility = var.visibility

  lifecycle {
    ignore_changes = [
      allow_rebase_merge,
      allow_squash_merge,
      allow_auto_merge,
      allow_merge_commit,
      delete_branch_on_merge,
      description,
      has_downloads,
      has_issues,
      has_projects,
      has_wiki,
      homepage_url,
      is_template,
      pages,
      template,
      topics,
      vulnerability_alerts,
    ]
  }
}

output "name" {
  value = var.name
}

output "is_private" {
  value = var.visibility != "public"
}
