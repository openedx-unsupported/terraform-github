// Terraform configuration-as-code for the Open edX GitHub organization!
//
// Required environment variables:
//
//  - GITHUB_TOKEN: A personal access token. Full org read access is
//    required for planning, and full or write access is requierd for
//    application
//
//  - GITHUB_OWNER: The name of the GitHub organization; in our case,
//    it should always be "openedx".
//    The docs claim that it can be set in the provider block, ie:
//        provider "github" { owner = "openedx" }
//    but it's a known issue that this doesn't always percolate down to
//    submodules, whereas GITHUB_OWNER reliably does.
//
//  - AWS_ACCESS_KEY_ID: AWS access key ID for use with S3 backend.
//
//  - AWS_ACCESS_KEY_SECRET: AWS secret key associated with
//    AWS_ACCESS_KEY_ID.

terraform {
  required_version = ">= 1.1.2"
  backend "s3" {
    encrypt                 = true
    bucket                  = "openedx-terraform-github-state"
    key                     = "state"
    dynamodb_table          = "terraform-state-lock"
    region                  = "us-east-1"
    skip_metadata_api_check = true
  }

  // Require the GitHub-maintained GitHub-Terraform provider.
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 4.0"
    }
  }
}

provider "github" {
}
