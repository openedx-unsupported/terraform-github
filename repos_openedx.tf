// Repositories within the Open edX organization.

// This file was automatically generated based on the contents of
// the 'openedx' GitHub organization as of 2021-11-30T17:10:49.133472.
// It is likely to be reorganized, refactored, split, or combined with
// other Terraform files in the near future.

module "repo_build_test_release_wg" {
  source = "./modules/repo"
  name   = "build-test-release-wg"
  phony = true
}

module "repo_community_wg" {
  source = "./modules/repo"
  name   = "community-wg"
  phony = true
}

module "repo_data_wg" {
  source = "./modules/repo"
  name   = "data-wg"
  phony = true
}

module "repo_frontend_wg" {
  source = "./modules/repo"
  name   = "frontend-wg"
  phony = true
}

module "repo_metrics_dashboard" {
  source = "./modules/repo"
  name   = "metrics-dashboard"
  phony = true
}

module "repo_olxcleaner" {
  source = "./modules/repo"
  name   = "olxcleaner"
  phony = true
}

module "repo_onboarding_course_introduction" {
  source = "./modules/repo"
  name   = "onboarding-course-introduction"
  phony = true
}

module "repo_openedx_conference_website" {
  source = "./modules/repo"
  name   = "openedx-conference-website"
  phony = true
}

module "repo_openedx_i18n" {
  source = "./modules/repo"
  name   = "openedx-i18n"
  phony = true
}

module "repo_openedx_slack_invite" {
  source = "./modules/repo"
  name   = "openedx-slack-invite"
  phony = true
}

module "repo_openedx_tech_radar" {
  source = "./modules/repo"
  name   = "openedx-tech-radar"
  phony = true
}

module "repo_platform_roadmap" {
  source = "./modules/repo"
  name   = "platform-roadmap"
  phony = true
}

module "repo_pr_watcher_notifier" {
  source = "./modules/repo"
  name   = "pr_watcher_notifier"
  phony = true
}

module "repo_public_engineering" {
  source = "./modules/repo"
  name   = "public-engineering"
  phony = true
}

module "repo_terraform_github" {
  source = "./modules/repo"
  name   = "terraform-github"
  phony = true
}
