// Roles, which grant an (ideally logical) collection of
// repository permissions to one or more Open edX organization users.

// This file was automatically generated based on the contents of
// the 'edxsolutions' GitHub organization as of 2021-11-29T15:16:32.751698.
// It is likely to be reorganized, refactored, split, or combined with
// other Terraform files in the near future.

module "role_edxsolutions_contributors" {
  source = "./modules/role"
  push_repos = [
    module.repo_xblock_adventure,
    module.repo_xblock_discussion,
    module.repo_xblock_drag_and_drop,
    module.repo_xblock_drag_and_drop_v2,
    module.repo_xblock_google_drive,
    module.repo_xblock_group_project,
    module.repo_xblock_image_explorer,
    module.repo_xblock_mentoring,
    module.repo_xblock_ooyala,
  ]
  users = [
    module.user_0x29a,
    module.user_agrendalath,
    module.user_ahmed_zubair12,
    module.user_ahtishamshahid,
    module.user_alex_sheehan_edx,
    module.user_antoviaque,
    module.user_attiyaishaque,
    module.user_awaisdar001,
    module.user_bradenmacdonald,
    module.user_clemente,
    module.user_davidjoy,
    module.user_gabrieldamours,
    module.user_giovannicimolin,
    module.user_jmbowman,
    module.user_jristau1984,
    module.user_kaizoku,
    module.user_kdmccormick,
    module.user_lgp171188,
    module.user_m_ali_0001,
    module.user_mattdrayer,
    module.user_moeez96,
    module.user_msaqib52,
    module.user_mudassir_hafeez,
    module.user_musmanmalik,
    module.user_nadeemshahzad,
    module.user_naeem91,
    module.user_nasirhjafri,
    module.user_natabene,
    module.user_nixknight,
    module.user_ormsbee,
    module.user_pomegranited,
    module.user_qasim_arbisoft,
    module.user_rgraber,
    module.user_shafqatfarhan,
    module.user_sohaibaslam,
    module.user_syed_awais_ali,
    module.user_syedimranhassan,
    module.user_viadanna,
    module.user_wasifarbisoft,
    module.user_xitij2000,
  ]
}

module "role_edxsolutions_core" {
  source = "./modules/role"
  admin_repos = [
    module.repo_xblock_adventure,
    module.repo_xblock_discussion,
    module.repo_xblock_drag_and_drop,
    module.repo_xblock_drag_and_drop_v2,
    module.repo_xblock_google_drive,
    module.repo_xblock_group_project,
    module.repo_xblock_image_explorer,
    module.repo_xblock_mentoring,
    module.repo_xblock_ooyala,
  ]
  users = [
    module.user_e0d,
    module.user_feanil,
    module.user_georgebabey,
    module.user_mattdrayer,
    module.user_nadeemshahzad,
    module.user_syedimranhassan,
  ]
}

module "role_edxsolutions_edx_platform_py3" {
  source = "./modules/role"
  push_repos = [
    module.repo_xblock_drag_and_drop_v2,
  ]
  users = [
    module.user_awais786,
    module.user_feanil,
  ]
}

module "role_edxsolutions_edx_solutions_admin" {
  source = "./modules/role"
  admin_repos = [
    module.repo_xblock_adventure,
    module.repo_xblock_discussion,
    module.repo_xblock_drag_and_drop,
    module.repo_xblock_drag_and_drop_v2,
    module.repo_xblock_google_drive,
    module.repo_xblock_group_project,
    module.repo_xblock_image_explorer,
    module.repo_xblock_mentoring,
    module.repo_xblock_ooyala,
  ]
  users = [
    module.user_adzuci,
    module.user_caplan188,
    module.user_e0d,
    module.user_edx_webhook,
    module.user_feanil,
    module.user_georgebabey,
    module.user_jdmulloy,
    module.user_kdmccormick,
    module.user_nadeemshahzad,
    module.user_natabene,
    module.user_nedbat,
    module.user_syedimranhassan,
    module.user_tnamgyal,
    module.user_wesmason,
  ]
}

module "role_edxsolutions_ooyala_xblock_contributors" {
  source = "./modules/role"
  push_repos = [
    module.repo_xblock_ooyala,
  ]
  users = [
    module.user_naeem91,
  ]
}

module "role_edxsolutions_travis_build_bot" {
  source = "./modules/role"
  admin_repos = [
    module.repo_xblock_drag_and_drop_v2,
    module.repo_xblock_mentoring,
  ]
  users = [
    module.user_edx_solutions_travis,
  ]
}

module "role_edxsolutions_user_dawoudsheraz" {
  source = "./modules/role"
  push_repos = [
    module.repo_xblock_drag_and_drop_v2,
  ]
  users = [
    module.user_dawoudsheraz,
  ]
}

module "role_edxsolutions_webhook_admin" {
  source = "./modules/role"
  admin_repos = [
    module.repo_xblock_drag_and_drop_v2,
    module.repo_xblock_google_drive,
  ]
  users = [
    module.user_edx_webhook,
  ]
}
