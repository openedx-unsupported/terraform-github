
variable "name" {
  type        = string
  description = "Name of the GitHub repository"
}

variable "visibility" {
  type        = string
  description = "Repository visibility ('public', 'private', or 'secret'. Defaults 'public')."
  default     = "public"
}

variable "ensure_commitlint" {
  type = bool
  description = "Whether or not this repo has the commitlint github action installed."
  default = "false"
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

data "github_repository" "repo" {
  name = github_repository.repo.name
  count = var.ensure_commitlint ? 1 : 0
}

data "github_repository_file" "commitlint_action" {
  repository = ".github"
  branch =  "master"
  file = "workflow-templates/commitlint.yml"

  count = var.ensure_commitlint ? 1 : 0
}

resource "github_repository_file" "commitlint_action" {
  repository = github_repository.repo.name
  branch =  data.github_repository.repo[0].default_branch
  file = ".github/workflows/commitlint.yml"
  content = data.github_repository_file.commitlint_action[0].content

  count = var.ensure_commitlint ? 1 : 0
}

output "name" {
  value = var.name
}

output "is_private" {
  value = var.visibility != "public"
}
