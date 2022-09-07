
module "decoupling" {
    source = "./modules/repo"
    name = "decoupling"
    visibility = "private"
}


module "openedx_wordpress_site" {
    source = "./modules/repo"
    name = "openedx-wordpress-site"
    visibility = "private"
}


module "terraform_internal" {
    source = "./modules/repo"
    name = "terraform-internal"
    visibility = "private"
}


module "tcril_interview" {
    source = "./modules/repo"
    name = "tcril-interview"
    visibility = "private"
}


module "openedx_webhooks_data" {
    source = "./modules/repo"
    name = "openedx-webhooks-data"
    visibility = "private"
}


module "tcril_interview_react_api" {
    source = "./modules/repo"
    name = "tcril-interview-react-api"
    visibility = "private"
}

