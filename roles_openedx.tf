// Roles, which grant an (ideally logical) collection of
// repository permissions to one or more Open edX organization users.

// This file was automatically generated based on the contents of
// the 'openedx' GitHub organization as of 2021-11-29T15:38:50.631605.
// It is likely to be reorganized, refactored, split, or combined with
// other Terraform files in the near future.

module "role_openedx_admin" {
  source = "./modules/role"
  admin_repos = [
    module.repo_build_test_release_wg,
    module.repo_community_wg,
    module.repo_data_wg,
    module.repo_frontend_wg,
    module.repo_metrics_dashboard,
    module.repo_olxcleaner,
    module.repo_onboarding_course_introduction,
    module.repo_openedx_conference_website,
    module.repo_openedx_i18n,
    module.repo_openedx_slack_invite,
    module.repo_openedx_tech_radar,
    module.repo_platform_roadmap,
    module.repo_pr_watcher_notifier,
    module.repo_public_engineering,
    module.repo_terraform_github,
  ]
  users = [
    module.user_davidjoy,
    module.user_e0d,
    module.user_feanil,
    module.user_jmbowman,
    module.user_kdmccormick,
    module.user_nedbat,
    module.user_ormsbee,
    module.user_sarina,
  ]
}

module "role_openedx_default_write_11_nov_2021" {
  source = "./modules/role"
  push_repos = [
    module.repo_build_test_release_wg,
    module.repo_community_wg,
    module.repo_data_wg,
    module.repo_frontend_wg,
    module.repo_metrics_dashboard,
    module.repo_olxcleaner,
    module.repo_onboarding_course_introduction,
    module.repo_openedx_conference_website,
    module.repo_openedx_i18n,
    module.repo_openedx_slack_invite,
    module.repo_openedx_tech_radar,
    module.repo_pr_watcher_notifier,
  ]
  users = [
    module.user_alangsto,
    module.user_arbrandes,
    module.user_bbrsofiane,
    module.user_carlos_muniz,
    module.user_davidjoy,
    module.user_e0d,
    module.user_edx_community_bot,
    module.user_ehuthmacher,
    module.user_feanil,
    module.user_jmbowman,
    module.user_jpbeaudry,
    module.user_kdmccormick,
    module.user_loucicchese,
    module.user_marcotuts,
    module.user_michellephilbrick,
    module.user_mulby,
    module.user_nedbat,
    module.user_omarithawi,
    module.user_ormsbee,
    module.user_regisb,
    module.user_sarina,
    module.user_shadinaif,
  ]
}

module "role_openedx_intro_course" {
  source = "./modules/role"
  push_repos = [
    module.repo_onboarding_course_introduction,
  ]
  users = [
    module.user_carlos_muniz,
    module.user_michellephilbrick,
    module.user_omarithawi,
    module.user_shadinaif,
  ]
}

module "role_openedx_tcril_engineering" {
  source = "./modules/role"
  push_repos = [
    module.repo_terraform_github,
  ]
  users = [
    module.user_carlos_muniz,
    module.user_feanil,
    module.user_kdmccormick,
    module.user_ormsbee,
    module.user_sarina,
  ]
}

module "role_openedx_user_adamstankiewicz" {
  source = "./modules/role"
  admin_repos = [
    module.repo_frontend_wg,
  ]
  users = [
    module.user_adamstankiewicz,
  ]
}

module "role_openedx_user_ahtishamshahid" {
  source = "./modules/role"
  push_repos = [
    module.repo_olxcleaner,
  ]
  users = [
    module.user_ahtishamshahid,
  ]
}

module "role_openedx_user_antoviaque" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_community_wg,
  ]
  users = [
    module.user_antoviaque,
  ]
}

module "role_openedx_user_arbrandes" {
  source = "./modules/role"
  admin_repos = [
    module.repo_build_test_release_wg,
    module.repo_community_wg,
  ]
  users = [
    module.user_arbrandes,
  ]
}

module "role_openedx_user_asadazam93" {
  source = "./modules/role"
  push_repos = [
    module.repo_olxcleaner,
  ]
  users = [
    module.user_asadazam93,
  ]
}

module "role_openedx_user_awaisdar001" {
  source = "./modules/role"
  admin_repos = [
    module.repo_olxcleaner,
  ]
  users = [
    module.user_awaisdar001,
  ]
}

module "role_openedx_user_bbrsofiane" {
  source = "./modules/role"
  admin_repos = [
    module.repo_build_test_release_wg,
  ]
  users = [
    module.user_bbrsofiane,
  ]
}

module "role_openedx_user_binodpant" {
  source = "./modules/role"
  admin_repos = [
    module.repo_frontend_wg,
  ]
  users = [
    module.user_binodpant,
  ]
}

module "role_openedx_user_bseverino" {
  source = "./modules/role"
  push_repos = [
    module.repo_frontend_wg,
  ]
  users = [
    module.user_bseverino,
  ]
}

module "role_openedx_user_cmltawt0" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_build_test_release_wg,
  ]
  users = [
    module.user_cmltawt0,
  ]
}

module "role_openedx_user_intro_course_bot" {
  source = "./modules/role"
  push_repos = [
    module.repo_onboarding_course_introduction,
  ]
  users = [
    module.user_intro_course_bot,
  ]
}

module "role_openedx_user_jazibhumayun" {
  source = "./modules/role"
  push_repos = [
    module.repo_metrics_dashboard,
  ]
  users = [
    module.user_jazibhumayun,
  ]
}

module "role_openedx_user_mdbc_tech" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_build_test_release_wg,
  ]
  users = [
    module.user_mdbc_tech,
  ]
}

module "role_openedx_user_muselesscreator" {
  source = "./modules/role"
  admin_repos = [
    module.repo_frontend_wg,
  ]
  users = [
    module.user_muselesscreator,
  ]
}

module "role_openedx_user_natabene" {
  source = "./modules/role"
  admin_repos = [
    module.repo_openedx_conference_website,
  ]
  users = [
    module.user_natabene,
  ]
}

module "role_openedx_user_nizarmah" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_community_wg,
  ]
  users = [
    module.user_nizarmah,
  ]
}

module "role_openedx_user_omarithawi" {
  source = "./modules/role"
  admin_repos = [
    module.repo_onboarding_course_introduction,
  ]
  users = [
    module.user_omarithawi,
  ]
}

module "role_openedx_user_pdpinch" {
  source = "./modules/role"
  admin_repos = [
    module.repo_olxcleaner,
  ]
  users = [
    module.user_pdpinch,
  ]
}

module "role_openedx_user_regisb" {
  source = "./modules/role"
  admin_repos = [
    module.repo_build_test_release_wg,
  ]
  users = [
    module.user_regisb,
  ]
}

module "role_openedx_user_saadyousafarbi" {
  source = "./modules/role"
  push_repos = [
    module.repo_olxcleaner,
  ]
  users = [
    module.user_saadyousafarbi,
  ]
}

module "role_openedx_user_schenedx" {
  source = "./modules/role"
  push_repos = [
    module.repo_data_wg,
  ]
  users = [
    module.user_schenedx,
  ]
}
