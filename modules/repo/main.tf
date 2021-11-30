
variable "name" {
  type        = string
  description = "Name of the GitHub repository"
}

variable "phony" {
  type        = bool
  default     = false
  description = "Whether this module instance should NOT be associated with a real GitHub repository. For use in TCRIL transition."
}

variable "visibility" {
  type        = string
  description = "Repository visibility ('public', 'private', or 'secret'. Defaults 'public')."
  default     = "public"
}

resource "github_repository" "this" {
  count = var.phony ? 0 : 1

  name       = var.name
  visibility = "public"

  lifecycle {
    ignore_changes = [
      allow_rebase_merge,
      allow_squash_merge,
      delete_branch_on_merge,
      description,
      has_downloads,
      has_issues,
      has_projects,
      has_wiki,
      vulnerability_alerts,
    ]
  }
}

output "phony" {
  value = var.phony
}

output "name" {
  value = var.name
}

output "is_private" {
  value = var.visibility != "public"
}
