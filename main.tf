terraform {
  required_version = ">= 1.0.11"
  backend "s3" {
    encrypt                 = true
    bucket                  = "openedx-terraform-github-state"
    key                     = "state"
    dynamodb_table          = "terraform-state-lock"
    region                  = "us-east-1"
    skip_metadata_api_check = true
  }
}

provider "github" {
  owner = "openedx"
}
