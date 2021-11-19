// Roles, which grant an (ideally logical) collection of
// repository permissions to one or more Open edX organization users.

// This file was automatically generated based on the contents of
// the 'edx' GitHub organization as of 2021-11-17T18:14:39.000000.
// It is likely to be reorganized, refactored, split, or combined with
// other Terraform files in the near future.

module "role_edx_account_edx_deployment_push" {
  source = "./modules/role"
  push_repos = [
    module.repo_acid_block,
    module.repo_edx_ui_toolkit,
    module.repo_frontend_app_publisher,
    module.repo_stylelint_config_edx,
    module.repo_xblock,
  ]
  users = [
    module.user_edx_deployment,
  ]
}

module "role_edx_admin" {
  source = "./modules/role"
  admin_repos = [
    module.repo_acclaimbadge_xblock,
    module.repo_acid_block,
    module.repo_animationxblock,
    module.repo_api_doc_tools,
    module.repo_audioxblock,
    module.repo_auth_backends,
    module.repo_blockstore,
    module.repo_bok_choy,
    module.repo_brand_openedx,
    module.repo_cc2olx,
    module.repo_ccx_keys,
    module.repo_code_annotations,
    module.repo_codejail,
    module.repo_completion,
    module.repo_conceptxblock,
    module.repo_configuration,
    module.repo_course_discovery,
    module.repo_credentials,
    module.repo_credentials_themes,
    module.repo_crowdsourcehinter,
    module.repo_cs_comments_service,
    module.repo_cypress_e2e_tests,
    module.repo_demo_performance_course,
    module.repo_demo_test_course,
    module.repo_devstack,
    module.repo_django_config_models,
    module.repo_django_lang_pref_middleware,
    module.repo_django_pyfs,
    module.repo_django_ratelimit_backend,
    module.repo_django_splash,
    module.repo_django_user_tasks,
    module.repo_django_wiki,
    module.repo_docs_dot_edx_dot_org,
    module.repo_donexblock,
    module.repo_dot_github,
    module.repo_ease,
    module.repo_ecommerce,
    module.repo_ecommerce_scripts,
    module.repo_ecommerce_worker,
    module.repo_edx4edx_lite,
    module.repo_edx_ace,
    module.repo_edx_analytics_configuration,
    module.repo_edx_analytics_dashboard,
    module.repo_edx_analytics_data_api,
    module.repo_edx_analytics_data_api_client,
    module.repo_edx_analytics_exporter,
    module.repo_edx_app_android,
    module.repo_edx_app_gradle_plugin,
    module.repo_edx_app_ios,
    module.repo_edx_app_test,
    module.repo_edx_bootstrap,
    module.repo_edx_bulk_grades,
    module.repo_edx_celeryutils,
    module.repo_edx_certificates,
    module.repo_edx_cookiecutters,
    module.repo_edx_custom_a11y_rules,
    module.repo_edx_demo_course,
    module.repo_edx_developer_docs,
    module.repo_edx_django_release_util,
    module.repo_edx_django_sites_extensions,
    module.repo_edx_django_utils,
    module.repo_edx_documentation,
    module.repo_edx_drf_extensions,
    module.repo_edx_enterprise,
    module.repo_edx_enterprise_data,
    module.repo_edx_lint,
    module.repo_edx_milestones,
    module.repo_edx_notes_api,
    module.repo_edx_notifications,
    module.repo_edx_ora2,
    module.repo_edx_organizations,
    module.repo_edx_platform,
    module.repo_edx_proctoring,
    module.repo_edx_rbac,
    module.repo_edx_repo_health,
    module.repo_edx_rest_api_client,
    module.repo_edx_search,
    module.repo_edx_sphinx_theme,
    module.repo_edx_submissions,
    module.repo_edx_toggles,
    module.repo_edx_tools,
    module.repo_edx_ui_toolkit,
    module.repo_edx_user_state_client,
    module.repo_edx_val,
    module.repo_edx_when,
    module.repo_edx_zoom,
    module.repo_enmerkar_underscore,
    module.repo_enterprise_catalog,
    module.repo_eslint_config,
    module.repo_eslint_config_edx,
    module.repo_event_routing_backends,
    module.repo_event_tracking,
    module.repo_frontend_app_account,
    module.repo_frontend_app_admin_portal,
    module.repo_frontend_app_authn,
    module.repo_frontend_app_course_authoring,
    module.repo_frontend_app_discussions,
    module.repo_frontend_app_ecommerce,
    module.repo_frontend_app_enterprise_public_catalog,
    module.repo_frontend_app_gradebook,
    module.repo_frontend_app_learner_portal_enterprise,
    module.repo_frontend_app_learner_portal_programs,
    module.repo_frontend_app_learning,
    module.repo_frontend_app_library_authoring,
    module.repo_frontend_app_payment,
    module.repo_frontend_app_profile,
    module.repo_frontend_app_program_console,
    module.repo_frontend_app_programs_dashboard,
    module.repo_frontend_app_publisher,
    module.repo_frontend_app_support_tools,
    module.repo_frontend_build,
    module.repo_frontend_component_cookie_policy_banner,
    module.repo_frontend_component_footer,
    module.repo_frontend_component_header,
    module.repo_frontend_enterprise,
    module.repo_frontend_learner_portal_base,
    module.repo_frontend_platform,
    module.repo_frontend_template_application,
    module.repo_help_tokens,
    module.repo_html_webpack_new_relic_plugin,
    module.repo_i18n_tools,
    module.repo_license_manager,
    module.repo_mdrst,
    module.repo_mockprock,
    module.repo_mongodbproxy,
    module.repo_opaque_keys,
    module.repo_open_edx_proposals,
    module.repo_openedx_calc,
    module.repo_openedx_census,
    module.repo_openedx_chem,
    module.repo_openedx_conference_pages,
    module.repo_openedx_webhooks,
    module.repo_openedxstats,
    module.repo_paragon,
    module.repo_pr_watcher_configuration,
    module.repo_pytest_repo_health,
    module.repo_pytest_warnings_report,
    module.repo_ratexblock,
    module.repo_reactifex,
    module.repo_recommenderxblock,
    module.repo_registrar,
    module.repo_repo_tools,
    module.repo_repo_tools_data_schema,
    module.repo_sample_themes,
    module.repo_schoolyourself_xblock,
    module.repo_staff_graded_xblock,
    module.repo_studio_frontend,
    module.repo_stylelint_config_edx,
    module.repo_super_csv,
    module.repo_taxonomy_connector,
    module.repo_tincanpython,
    module.repo_tinymce_language_selector,
    module.repo_tubular,
    module.repo_user_util,
    module.repo_web_fragments,
    module.repo_webhook_test_repo,
    module.repo_xblock,
    module.repo_xblock_free_text_response,
    module.repo_xblock_image_modal,
    module.repo_xblock_in_video_quiz,
    module.repo_xblock_lti_consumer,
    module.repo_xblock_qualtrics_survey,
    module.repo_xblock_sdk,
    module.repo_xblock_sql_grader,
    module.repo_xblock_submit_and_compare,
    module.repo_xblock_utils,
    module.repo_xqueue,
    module.repo_xqueue_watcher,
    module.repo_xss_utils,
  ]
  users = [
    module.user_adzuci,
    module.user_arbabkhalil,
    module.user_augustoverride,
    module.user_caplan188,
    module.user_christopappas,
    module.user_davidjoy,
    module.user_dianakhuang,
    module.user_e0d,
    module.user_edx_github_actions_runner,
    module.user_edx_webhook,
    module.user_estute,
    module.user_feanil,
    module.user_jazibhumayun,
    module.user_jdmulloy,
    module.user_jmbowman,
    module.user_kdmccormick,
    module.user_loucicchese,
    module.user_matthugs,
    module.user_mulby,
    module.user_nadeemshahzad,
    module.user_nedbat,
    module.user_nixknight,
    module.user_ormsbee,
    module.user_robrap,
    module.user_saleem_latif,
    module.user_sarina,
    module.user_syed_awais_ali,
    module.user_syedimranhassan,
    module.user_tnamgyal,
    module.user_tuchfarber,
    module.user_wesmason,
  ]
}

module "role_edx_analytics_admin" {
  source = "./modules/role"
  admin_repos = [
    module.repo_edx_analytics_configuration,
    module.repo_edx_analytics_dashboard,
    module.repo_edx_analytics_data_api,
    module.repo_edx_analytics_data_api_client,
    module.repo_edx_analytics_exporter,
  ]
  users = [
    module.user_macdiesel,
  ]
}

module "role_edx_analytics_arbisoft_push" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_analytics_configuration,
  ]
  users = [
    module.user_hassanjaveed84,
  ]
}

module "role_edx_analytics_push" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_analytics_configuration,
    module.repo_edx_analytics_dashboard,
    module.repo_edx_analytics_data_api,
    module.repo_edx_analytics_data_api_client,
    module.repo_event_tracking,
  ]
  users = [
    module.user_ahsanshafiq742,
    module.user_bmedx,
    module.user_brianhw,
    module.user_debbiejacob,
    module.user_doctoryes,
    module.user_e0d,
    module.user_edx_analytics_automation,
    module.user_estute,
    module.user_macdiesel,
    module.user_mulby,
    module.user_openedx_release_bot,
    module.user_pwnage101,
    module.user_usama101,
  ]
}

module "role_edx_aperture" {
  source = "./modules/role"
  push_repos = [
    module.repo_credentials,
    module.repo_credentials_themes,
  ]
  users = [
    module.user_georgebabey,
    module.user_justinhynes,
    module.user_oliviaruizknott,
    module.user_tj_tracy,
    module.user_tuchfarber,
  ]
}

module "role_edx_arbi_bom" {
  source = "./modules/role"
  admin_repos = [
    module.repo_devstack,
  ]
  maintain_repos = [
    module.repo_event_routing_backends,
  ]
  push_repos = [
    module.repo_auth_backends,
    module.repo_bok_choy,
    module.repo_django_config_models,
    module.repo_django_lang_pref_middleware,
    module.repo_django_user_tasks,
    module.repo_django_wiki,
    module.repo_edx_ace,
    module.repo_edx_celeryutils,
    module.repo_edx_cookiecutters,
    module.repo_edx_django_utils,
    module.repo_edx_drf_extensions,
    module.repo_edx_lint,
    module.repo_edx_organizations,
    module.repo_edx_platform,
    module.repo_edx_rbac,
    module.repo_edx_repo_health,
    module.repo_edx_rest_api_client,
    module.repo_edx_sphinx_theme,
    module.repo_edx_toggles,
    module.repo_event_tracking,
    module.repo_opaque_keys,
    module.repo_open_edx_proposals,
    module.repo_pytest_repo_health,
    module.repo_repo_tools,
    module.repo_xblock,
    module.repo_xblock_utils,
    module.repo_xqueue,
    module.repo_xss_utils,
  ]
  users = [
    module.user_awais786,
    module.user_iamsobanjaved,
    module.user_jmbowman,
    module.user_mraarif,
    module.user_usamasadiq,
  ]
}

module "role_edx_arch_bom" {
  source = "./modules/role"
  admin_repos = [
    module.repo_auth_backends,
    module.repo_bok_choy,
    module.repo_brand_openedx,
    module.repo_ccx_keys,
    module.repo_devstack,
    module.repo_django_config_models,
    module.repo_django_lang_pref_middleware,
    module.repo_django_pyfs,
    module.repo_django_splash,
    module.repo_django_user_tasks,
    module.repo_edx4edx_lite,
    module.repo_edx_bootstrap,
    module.repo_edx_celeryutils,
    module.repo_edx_cookiecutters,
    module.repo_edx_custom_a11y_rules,
    module.repo_edx_django_utils,
    module.repo_edx_drf_extensions,
    module.repo_edx_lint,
    module.repo_edx_platform,
    module.repo_edx_rbac,
    module.repo_edx_repo_health,
    module.repo_edx_rest_api_client,
    module.repo_edx_toggles,
    module.repo_edx_tools,
    module.repo_enmerkar_underscore,
    module.repo_event_routing_backends,
    module.repo_frontend_platform,
    module.repo_help_tokens,
    module.repo_html_webpack_new_relic_plugin,
    module.repo_open_edx_proposals,
    module.repo_openedx_calc,
    module.repo_pytest_repo_health,
    module.repo_pytest_warnings_report,
    module.repo_repo_tools,
    module.repo_web_fragments,
    module.repo_xblock_lti_consumer,
    module.repo_xss_utils,
  ]
  push_repos = [
    module.repo_edx_organizations,
    module.repo_edx_sphinx_theme,
    module.repo_opaque_keys,
    module.repo_xblock,
    module.repo_xblock_utils,
  ]
  users = [
    module.user_davidjoy,
    module.user_dianakhuang,
    module.user_jinder1s,
    module.user_jmbowman,
    module.user_nedbat,
    module.user_rgraber,
    module.user_robrap,
    module.user_timmc_edx,
  ]
}

module "role_edx_bok_choy_push" {
  source = "./modules/role"
  push_repos = [
    module.repo_bok_choy,
  ]
  users = [
    module.user_muhammad_ammar,
  ]
}

module "role_edx_business_enterprise_team" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_enterprise,
    module.repo_enterprise_catalog,
  ]
  users = [
    module.user_adamstankiewicz,
    module.user_alex_sheehan_edx,
    module.user_binodpant,
    module.user_christopappas,
    module.user_georgebabey,
    module.user_iloveagent57,
    module.user_irfanuddinahmad,
    module.user_johnnagro,
    module.user_kiram15,
    module.user_long74100,
    module.user_macdiesel,
    module.user_manny_m,
    module.user_moconnell1453,
    module.user_muhammad_ammar,
    module.user_zamanafzal,
  ]
}

module "role_edx_cache_uploader_bot" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_django_utils,
    module.repo_edx_platform,
    module.repo_xss_utils,
  ]
  users = [
    module.user_edx_cache_uploader_bot,
  ]
}

module "role_edx_ccp_committer_agrendalath" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_edx_platform,
    module.repo_xblock_lti_consumer,
  ]
  users = [
    module.user_agrendalath,
  ]
}

module "role_edx_ccp_committer_arbrandes" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_platform,
    module.repo_frontend_app_library_authoring,
  ]
  users = [
    module.user_arbrandes,
  ]
}

module "role_edx_ccp_committer_bbrsofiane" {
  source = "./modules/role"
  push_repos = [
    module.repo_frontend_app_gradebook,
    module.repo_frontend_app_learning,
    module.repo_frontend_app_profile,
    module.repo_frontend_build,
    module.repo_frontend_platform,
  ]
  users = [
    module.user_bbrsofiane,
  ]
}

module "role_edx_ccp_committer_bradenmacdonald" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_blockstore,
    module.repo_edx_platform,
    module.repo_opaque_keys,
    module.repo_xblock,
    module.repo_xblock_sdk,
    module.repo_xblock_utils,
  ]
  users = [
    module.user_bradenmacdonald,
  ]
}

module "role_edx_ccp_committer_cmltawt0" {
  source = "./modules/role"
  push_repos = [
    module.repo_cypress_e2e_tests,
    module.repo_devstack,
    module.repo_edx_app_test,
  ]
  users = [
    module.user_cmltawt0,
  ]
}

module "role_edx_ccp_committer_felipemontoya" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_edx_django_utils,
    module.repo_edx_platform,
    module.repo_opaque_keys,
    module.repo_xblock,
    module.repo_xblock_sdk,
    module.repo_xblock_utils,
  ]
  users = [
    module.user_felipemontoya,
  ]
}

module "role_edx_ccp_committer_giovannicimolin" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_platform,
    module.repo_xblock_lti_consumer,
  ]
  users = [
    module.user_giovannicimolin,
  ]
}

module "role_edx_ccp_committer_idegtiarov" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_auth_backends,
    module.repo_edx_organizations,
    module.repo_edx_proctoring,
    module.repo_edx_rbac,
    module.repo_edx_rest_api_client,
    module.repo_edx_search,
    module.repo_xblock_lti_consumer,
  ]
  users = [
    module.user_idegtiarov,
  ]
}

module "role_edx_ccp_committer_jfavellar90" {
  source = "./modules/role"
  push_repos = [
    module.repo_configuration,
  ]
  users = [
    module.user_jfavellar90,
    module.user_sarina,
  ]
}

module "role_edx_ccp_committer_omarithawi" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_edx_ace,
  ]
  users = [
    module.user_omarithawi,
  ]
}

module "role_edx_ccp_committer_pdpinch" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_ccx_keys,
    module.repo_edx_platform,
    module.repo_opaque_keys,
    module.repo_xblock,
    module.repo_xblock_sdk,
    module.repo_xblock_utils,
  ]
  users = [
    module.user_pdpinch,
  ]
}

module "role_edx_ccp_committer_pomegranited" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_configuration,
    module.repo_edx_ora2,
  ]
  users = [
    module.user_pomegranited,
  ]
}

module "role_edx_ccp_committer_regisb" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_code_annotations,
    module.repo_devstack,
    module.repo_django_config_models,
    module.repo_edx_django_utils,
    module.repo_edx_toggles,
  ]
  users = [
    module.user_regisb,
  ]
}

module "role_edx_ccp_committer_symbolist" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_blockstore,
    module.repo_xblock,
    module.repo_xblock_sdk,
    module.repo_xblock_utils,
  ]
  users = [
    module.user_symbolist,
  ]
}

module "role_edx_ccp_committer_xitij2000" {
  source = "./modules/role"
  push_repos = [
    module.repo_cs_comments_service,
    module.repo_frontend_app_course_authoring,
    module.repo_frontend_app_discussions,
    module.repo_xblock_lti_consumer,
  ]
  users = [
    module.user_xitij2000,
  ]
}

module "role_edx_ccp_committer_ziafazal" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_edx_platform,
    module.repo_event_routing_backends,
  ]
  users = [
    module.user_ziafazal,
  ]
}

module "role_edx_codecov_bot" {
  source = "./modules/role"
  push_repos = [
    module.repo_devstack,
  ]
  users = [
    module.user_edx_codecov_bot,
  ]
}

module "role_edx_community_bot" {
  source = "./modules/role"
  admin_repos = [
    module.repo_configuration,
    module.repo_cypress_e2e_tests,
    module.repo_devstack,
    module.repo_edx_app_test,
    module.repo_edx_platform,
    module.repo_open_edx_proposals,
  ]
  users = [
    module.user_edx_community_bot,
  ]
}

module "role_edx_community_engineering" {
  source = "./modules/role"
  admin_repos = [
    module.repo_acclaimbadge_xblock,
    module.repo_acid_block,
    module.repo_animationxblock,
    module.repo_api_doc_tools,
    module.repo_audioxblock,
    module.repo_ccx_keys,
    module.repo_conceptxblock,
    module.repo_crowdsourcehinter,
    module.repo_docs_dot_edx_dot_org,
    module.repo_donexblock,
    module.repo_dot_github,
    module.repo_edx_bootstrap,
    module.repo_edx_developer_docs,
    module.repo_edx_documentation,
    module.repo_edx_sphinx_theme,
    module.repo_edx_ui_toolkit,
    module.repo_eslint_config,
    module.repo_eslint_config_edx,
    module.repo_frontend_app_account,
    module.repo_frontend_app_profile,
    module.repo_frontend_component_footer,
    module.repo_frontend_component_header,
    module.repo_frontend_platform,
    module.repo_frontend_template_application,
    module.repo_html_webpack_new_relic_plugin,
    module.repo_mdrst,
    module.repo_openedx_census,
    module.repo_openedx_conference_pages,
    module.repo_openedx_webhooks,
    module.repo_openedxstats,
    module.repo_pr_watcher_configuration,
    module.repo_ratexblock,
    module.repo_recommenderxblock,
    module.repo_repo_tools_data_schema,
    module.repo_sample_themes,
    module.repo_schoolyourself_xblock,
    module.repo_staff_graded_xblock,
    module.repo_stylelint_config_edx,
    module.repo_webhook_test_repo,
    module.repo_xblock_free_text_response,
    module.repo_xblock_image_modal,
    module.repo_xblock_in_video_quiz,
    module.repo_xblock_lti_consumer,
    module.repo_xblock_qualtrics_survey,
    module.repo_xblock_sql_grader,
    module.repo_xblock_submit_and_compare,
  ]
  push_repos = [
    module.repo_edx_platform,
  ]
  users = [
    module.user_davidjoy,
    module.user_nedbat,
  ]
}

module "role_edx_community_release_managers" {
  source = "./modules/role"
  push_repos = [
    module.repo_blockstore,
    module.repo_configuration,
    module.repo_course_discovery,
    module.repo_credentials,
    module.repo_cs_comments_service,
    module.repo_devstack,
    module.repo_ecommerce,
    module.repo_ecommerce_worker,
    module.repo_edx_analytics_configuration,
    module.repo_edx_analytics_dashboard,
    module.repo_edx_analytics_data_api,
    module.repo_edx_app_android,
    module.repo_edx_app_ios,
    module.repo_edx_certificates,
    module.repo_edx_demo_course,
    module.repo_edx_developer_docs,
    module.repo_edx_documentation,
    module.repo_edx_notes_api,
    module.repo_edx_platform,
    module.repo_enterprise_catalog,
    module.repo_frontend_app_account,
    module.repo_frontend_app_authn,
    module.repo_frontend_app_discussions,
    module.repo_frontend_app_ecommerce,
    module.repo_frontend_app_gradebook,
    module.repo_frontend_app_learning,
    module.repo_frontend_app_library_authoring,
    module.repo_frontend_app_payment,
    module.repo_frontend_app_profile,
    module.repo_frontend_app_publisher,
    module.repo_frontend_app_support_tools,
    module.repo_frontend_template_application,
    module.repo_license_manager,
    module.repo_repo_tools,
    module.repo_tubular,
    module.repo_xqueue,
  ]
  users = [
    module.user_nedbat,
  ]
}

module "role_edx_core_contributor_program_committers" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_open_edx_proposals,
  ]
  users = [
    module.user_agrendalath,
    module.user_arbrandes,
    module.user_bbrsofiane,
    module.user_bradenmacdonald,
    module.user_cmltawt0,
    module.user_edx_community_bot,
    module.user_felipemontoya,
    module.user_giovannicimolin,
    module.user_idegtiarov,
    module.user_jfavellar90,
    module.user_omarithawi,
    module.user_pdpinch,
    module.user_pomegranited,
    module.user_regisb,
    module.user_sarina,
    module.user_symbolist,
    module.user_xitij2000,
    module.user_ziafazal,
  ]
}

module "role_edx_course_discovery_admins" {
  source = "./modules/role"
  admin_repos = [
    module.repo_course_discovery,
    module.repo_frontend_app_publisher,
  ]
  users = [
    module.user_adeelehsan,
    module.user_albemarle,
    module.user_attiyaishaque,
    module.user_mubbsharanwar,
    module.user_shafqatfarhan,
    module.user_uzairr,
    module.user_waheedahmed,
    module.user_zainab_amir,
  ]
}

module "role_edx_data_engineering" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_analytics_dashboard,
    module.repo_edx_analytics_data_api,
  ]
  users = [
    module.user_ark_edly,
    module.user_brianhw,
    module.user_estute,
    module.user_hassanjaveed84,
    module.user_jazibhumayun,
    module.user_macdiesel,
    module.user_pwnage101,
  ]
}

module "role_edx_devops" {
  source = "./modules/role"
  admin_repos = [
    module.repo_tubular,
    module.repo_xqueue,
  ]
  push_repos = [
    module.repo_configuration,
    module.repo_edx_notes_api,
    module.repo_xss_utils,
  ]
  users = [
    module.user_adzuci,
    module.user_arbabkhalil,
    module.user_christopappas,
    module.user_jdmulloy,
    module.user_loucicchese,
    module.user_nadeemshahzad,
    module.user_nixknight,
    module.user_oel8man,
    module.user_syed_awais_ali,
    module.user_syedimranhassan,
  ]
}

module "role_edx_ecommerce" {
  source = "./modules/role"
  admin_repos = [
    module.repo_edx_rest_api_client,
  ]
  push_repos = [
    module.repo_frontend_app_ecommerce,
    module.repo_frontend_app_payment,
  ]
  users = [
    module.user_dianekaplan,
    module.user_georgebabey,
    module.user_inventhouse,
    module.user_jmyatt,
    module.user_julianajlk,
    module.user_matthewpiatetsky,
    module.user_mulby,
    module.user_pshiu,
    module.user_robrap,
    module.user_waheedahmed,
  ]
}

module "role_edx_engage_squad" {
  source = "./modules/role"
  admin_repos = [
    module.repo_completion,
    module.repo_django_wiki,
    module.repo_edx_ace,
    module.repo_edx_user_state_client,
    module.repo_edx_when,
    module.repo_frontend_app_learning,
    module.repo_tinymce_language_selector,
  ]
  users = [
    module.user_cdeery,
    module.user_ciduarte,
    module.user_dillon_dumesnil,
    module.user_jmyatt,
    module.user_matthewpiatetsky,
    module.user_mikix,
  ]
}

module "role_edx_enterprise_catalog_admins" {
  source = "./modules/role"
  admin_repos = [
    module.repo_enterprise_catalog,
    module.repo_license_manager,
  ]
  users = [
    module.user_adamstankiewicz,
    module.user_georgebabey,
    module.user_iloveagent57,
  ]
}

module "role_edx_enterprise_markhors" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_taxonomy_connector,
  ]
  users = [
    module.user_hammadahmadwaqas,
    module.user_irfanuddinahmad,
    module.user_moconnell1453,
    module.user_muhammad_ammar,
    module.user_saleem_latif,
    module.user_sameenfatima78,
    module.user_zamanafzal,
  ]
}

module "role_edx_enterprise_online_campus" {
  source = "./modules/role"
  admin_repos = [
    module.repo_frontend_app_enterprise_public_catalog,
  ]
  push_repos = [
    module.repo_edx_analytics_data_api,
    module.repo_edx_enterprise,
    module.repo_edx_enterprise_data,
    module.repo_frontend_app_admin_portal,
    module.repo_frontend_app_learner_portal_enterprise,
  ]
  users = [
    module.user_alex_sheehan_edx,
    module.user_binodpant,
    module.user_georgebabey,
    module.user_johnnagro,
    module.user_kiram15,
  ]
}

module "role_edx_enterprise_titans" {
  source = "./modules/role"
  admin_repos = [
    module.repo_license_manager,
  ]
  push_repos = [
    module.repo_enterprise_catalog,
  ]
  users = [
    module.user_adamstankiewicz,
    module.user_binodpant,
    module.user_christopappas,
    module.user_iloveagent57,
    module.user_long74100,
    module.user_macdiesel,
    module.user_manny_m,
  ]
}

module "role_edx_fedx_admin" {
  source = "./modules/role"
  admin_repos = [
    module.repo_edx_bootstrap,
    module.repo_edx_ui_toolkit,
    module.repo_eslint_config,
    module.repo_eslint_config_edx,
    module.repo_frontend_app_enterprise_public_catalog,
    module.repo_frontend_app_learner_portal_enterprise,
    module.repo_frontend_build,
    module.repo_frontend_enterprise,
    module.repo_frontend_learner_portal_base,
    module.repo_paragon,
    module.repo_stylelint_config_edx,
    module.repo_web_fragments,
  ]
  users = [
    module.user_adamstankiewicz,
    module.user_davidjoy,
  ]
}

module "role_edx_fedx_team" {
  source = "./modules/role"
  admin_repos = [
    module.repo_brand_openedx,
    module.repo_edx_bootstrap,
    module.repo_frontend_build,
    module.repo_frontend_template_application,
  ]
  push_repos = [
    module.repo_edx_django_utils,
    module.repo_edx_ui_toolkit,
    module.repo_eslint_config,
    module.repo_frontend_app_learning,
    module.repo_paragon,
    module.repo_stylelint_config_edx,
  ]
  users = [
    module.user_adamstankiewicz,
    module.user_davidjoy,
    module.user_georgebabey,
    module.user_julianajlk,
    module.user_justinhynes,
    module.user_matthugs,
    module.user_michaelroytman,
    module.user_mikix,
    module.user_muselesscreator,
    module.user_tj_tracy,
    module.user_wittjeff,
  ]
}

module "role_edx_github_pages_only" {
  source = "./modules/role"
  admin_repos = [
    module.repo_openedx_conference_pages,
  ]
  users = [
    module.user_nedbat,
  ]
}

module "role_edx_incident_management" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_val,
  ]
  users = [
    module.user_ali_d_akbar,
    module.user_ansabgillani,
    module.user_azanbinzahid,
    module.user_dawoudsheraz,
    module.user_kashifch,
  ]
}

module "role_edx_incr_reviewers" {
  source = "./modules/role"
  push_repos = [
    module.repo_acid_block,
    module.repo_codejail,
    module.repo_edx_analytics_data_api_client,
    module.repo_edx_lint,
    module.repo_edx_milestones,
    module.repo_edx_search,
    module.repo_edx_submissions,
    module.repo_edx_user_state_client,
    module.repo_edx_val,
    module.repo_event_tracking,
    module.repo_web_fragments,
    module.repo_xblock_sdk,
    module.repo_xblock_utils,
  ]
  users = [
    module.user_awais786,
    module.user_estute,
    module.user_jmbowman,
    module.user_mraarif,
  ]
}

module "role_edx_learner_admins" {
  source = "./modules/role"
  admin_repos = [
    module.repo_auth_backends,
    module.repo_credentials,
    module.repo_credentials_themes,
    module.repo_devstack,
    module.repo_edx_drf_extensions,
    module.repo_edx_rest_api_client,
  ]
  users = [
    module.user_jmyatt,
  ]
}

module "role_edx_masters_admins" {
  source = "./modules/role"
  admin_repos = [
    module.repo_completion,
    module.repo_edx_ora2,
    module.repo_edx_proctoring,
  ]
  users = [
    module.user_mattcarter,
    module.user_schenedx,
  ]
}

module "role_edx_masters_all" {
  source = "./modules/role"
  admin_repos = [
    module.repo_completion,
  ]
  users = [
    module.user_alangsto,
    module.user_ashultz0,
    module.user_bseverino,
    module.user_iloveagent57,
    module.user_jansenk,
    module.user_katymyw,
    module.user_mattcarter,
    module.user_matthugs,
    module.user_michaelroytman,
    module.user_nsprenkle,
    module.user_schenedx,
    module.user_zacharis278,
  ]
}

module "role_edx_masters_dahlia" {
  source = "./modules/role"
  admin_repos = [
    module.repo_studio_frontend,
  ]
  push_repos = [
    module.repo_edx_bulk_grades,
    module.repo_edx_zoom,
    module.repo_super_csv,
  ]
  users = [
    module.user_iloveagent57,
    module.user_jansenk,
    module.user_matthugs,
    module.user_michaelroytman,
    module.user_nsprenkle,
  ]
}

module "role_edx_masters_devs" {
  source = "./modules/role"
  push_repos = [
    module.repo_completion,
    module.repo_credentials,
    module.repo_edx_proctoring,
    module.repo_frontend_app_course_authoring,
    module.repo_registrar,
  ]
  users = [
    module.user_alangsto,
    module.user_ashultz0,
    module.user_bseverino,
    module.user_jansenk,
    module.user_jnlapierre,
    module.user_leangseu_edx,
    module.user_mattcarter,
    module.user_matthugs,
    module.user_michaelroytman,
    module.user_muselesscreator,
    module.user_nsprenkle,
    module.user_schenedx,
    module.user_zacharis278,
  ]
}

module "role_edx_masters_devs_cosmonauts" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_edx_analytics_data_api,
  ]
  push_repos = [
    module.repo_cc2olx,
    module.repo_edx_analytics_dashboard,
  ]
  users = [
    module.user_alangsto,
    module.user_ashultz0,
    module.user_bseverino,
    module.user_matthugs,
    module.user_michaelroytman,
    module.user_schenedx,
    module.user_zacharis278,
  ]
}

module "role_edx_masters_devs_gta" {
  source = "./modules/role"
  admin_repos = [
    module.repo_edx_ora2,
  ]
  maintain_repos = [
    module.repo_edx_bulk_grades,
  ]
  push_repos = [
    module.repo_super_csv,
  ]
  users = [
    module.user_jansenk,
    module.user_jnlapierre,
    module.user_leangseu_edx,
    module.user_mattcarter,
    module.user_matthugs,
    module.user_muselesscreator,
    module.user_nsprenkle,
  ]
}

module "role_edx_masters_mm_dev" {
  source = "./modules/role"
  admin_repos = [
    module.repo_credentials,
    module.repo_frontend_app_program_console,
    module.repo_registrar,
  ]
  users = [
    module.user_alangsto,
    module.user_ashultz0,
    module.user_iloveagent57,
    module.user_jansenk,
    module.user_mattcarter,
    module.user_matthugs,
    module.user_michaelroytman,
    module.user_nsprenkle,
    module.user_schenedx,
    module.user_zacharis278,
  ]
}

module "role_edx_milestones" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_milestones,
  ]
  users = [
    module.user_antoviaque,
    module.user_macdiesel,
    module.user_mattdrayer,
    module.user_muhammad_ammar,
    module.user_mulby,
    module.user_ormsbee,
  ]
}

module "role_edx_mobile_admin" {
  source = "./modules/role"
  admin_repos = [
    module.repo_edx_app_android,
    module.repo_edx_app_ios,
    module.repo_edx_app_test,
  ]
  users = [
    module.user_colinbrash,
    module.user_mulby,
  ]
}

module "role_edx_mobile_push" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_app_android,
    module.repo_edx_app_gradle_plugin,
    module.repo_edx_app_ios,
    module.repo_edx_app_test,
  ]
  users = [
    module.user_bilalawan321,
    module.user_colinbrash,
    module.user_edx_travis_rw,
    module.user_farhan_arshad_dev,
    module.user_hamzaisrar_arbisoft,
    module.user_jawad_khan,
    module.user_miankhalid,
    module.user_mulby,
    module.user_mumer92,
    module.user_omerhabib26,
    module.user_saeedbashir,
  ]
}

module "role_edx_open_source_team" {
  source = "./modules/role"
  push_repos = [
    module.repo_openedxstats,
  ]
  users = [
    module.user_nedbat,
  ]
}

module "role_edx_openedx_support_team" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_app_android,
  ]
  users = [
    module.user_natabene,
  ]
}

module "role_edx_openedx_tooling" {
  source = "./modules/role"
  admin_repos = [
    module.repo_openedx_webhooks,
  ]
  users = [
    module.user_nedbat,
  ]
}

module "role_edx_ora2_push" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_ora2,
  ]
  users = [
    module.user_dianakhuang,
    module.user_jaakana,
  ]
}

module "role_edx_paragon_working_group" {
  source = "./modules/role"
  push_repos = [
    module.repo_paragon,
  ]
  users = [
    module.user_adamstankiewicz,
    module.user_ciduarte,
    module.user_davidjoy,
    module.user_edx_netlify,
    module.user_georgebabey,
    module.user_long74100,
    module.user_manny_m,
    module.user_marcotuts,
    module.user_muselesscreator,
    module.user_wittjeff,
  ]
}

module "role_edx_pipeline_bot" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_platform,
    module.repo_frontend_app_publisher,
    module.repo_xss_utils,
  ]
  users = [
    module.user_edx_pipeline_bot,
    module.user_edx_secure,
  ]
}

module "role_edx_pipeline_team" {
  source = "./modules/role"
  admin_repos = [
    module.repo_tubular,
  ]
  users = [
    module.user_doctoryes,
    module.user_e0d,
    module.user_estute,
    module.user_feanil,
    module.user_jdmulloy,
    module.user_macdiesel,
    module.user_matthewpiatetsky,
    module.user_matthugs,
    module.user_nadeemshahzad,
    module.user_srwang,
    module.user_tuchfarber,
  ]
}

module "role_edx_programs_admin" {
  source = "./modules/role"
  admin_repos = [
    module.repo_credentials,
    module.repo_frontend_app_learner_portal_programs,
  ]
  users = [
    module.user_schenedx,
  ]
}

module "role_edx_push_pull_all" {
  source = "./modules/role"
  push_repos = [
    module.repo_acclaimbadge_xblock,
    module.repo_acid_block,
    module.repo_animationxblock,
    module.repo_api_doc_tools,
    module.repo_audioxblock,
    module.repo_auth_backends,
    module.repo_blockstore,
    module.repo_bok_choy,
    module.repo_brand_openedx,
    module.repo_cc2olx,
    module.repo_ccx_keys,
    module.repo_code_annotations,
    module.repo_codejail,
    module.repo_completion,
    module.repo_conceptxblock,
    module.repo_configuration,
    module.repo_course_discovery,
    module.repo_credentials,
    module.repo_credentials_themes,
    module.repo_crowdsourcehinter,
    module.repo_cs_comments_service,
    module.repo_cypress_e2e_tests,
    module.repo_demo_performance_course,
    module.repo_demo_test_course,
    module.repo_devstack,
    module.repo_django_config_models,
    module.repo_django_lang_pref_middleware,
    module.repo_django_pyfs,
    module.repo_django_ratelimit_backend,
    module.repo_django_splash,
    module.repo_django_user_tasks,
    module.repo_django_wiki,
    module.repo_docs_dot_edx_dot_org,
    module.repo_donexblock,
    module.repo_dot_github,
    module.repo_ease,
    module.repo_ecommerce,
    module.repo_ecommerce_scripts,
    module.repo_ecommerce_worker,
    module.repo_edx4edx_lite,
    module.repo_edx_ace,
    module.repo_edx_analytics_dashboard,
    module.repo_edx_analytics_data_api,
    module.repo_edx_analytics_data_api_client,
    module.repo_edx_analytics_exporter,
    module.repo_edx_app_gradle_plugin,
    module.repo_edx_bootstrap,
    module.repo_edx_bulk_grades,
    module.repo_edx_celeryutils,
    module.repo_edx_certificates,
    module.repo_edx_cookiecutters,
    module.repo_edx_custom_a11y_rules,
    module.repo_edx_demo_course,
    module.repo_edx_developer_docs,
    module.repo_edx_django_release_util,
    module.repo_edx_django_sites_extensions,
    module.repo_edx_django_utils,
    module.repo_edx_documentation,
    module.repo_edx_drf_extensions,
    module.repo_edx_enterprise,
    module.repo_edx_enterprise_data,
    module.repo_edx_lint,
    module.repo_edx_milestones,
    module.repo_edx_notes_api,
    module.repo_edx_notifications,
    module.repo_edx_ora2,
    module.repo_edx_organizations,
    module.repo_edx_platform,
    module.repo_edx_proctoring,
    module.repo_edx_rbac,
    module.repo_edx_repo_health,
    module.repo_edx_rest_api_client,
    module.repo_edx_search,
    module.repo_edx_sphinx_theme,
    module.repo_edx_submissions,
    module.repo_edx_toggles,
    module.repo_edx_tools,
    module.repo_edx_ui_toolkit,
    module.repo_edx_user_state_client,
    module.repo_edx_val,
    module.repo_edx_when,
    module.repo_edx_zoom,
    module.repo_enmerkar_underscore,
    module.repo_enterprise_catalog,
    module.repo_eslint_config,
    module.repo_event_routing_backends,
    module.repo_event_tracking,
    module.repo_frontend_app_account,
    module.repo_frontend_app_admin_portal,
    module.repo_frontend_app_authn,
    module.repo_frontend_app_course_authoring,
    module.repo_frontend_app_discussions,
    module.repo_frontend_app_ecommerce,
    module.repo_frontend_app_enterprise_public_catalog,
    module.repo_frontend_app_gradebook,
    module.repo_frontend_app_learner_portal_enterprise,
    module.repo_frontend_app_learner_portal_programs,
    module.repo_frontend_app_learning,
    module.repo_frontend_app_library_authoring,
    module.repo_frontend_app_payment,
    module.repo_frontend_app_profile,
    module.repo_frontend_app_program_console,
    module.repo_frontend_app_programs_dashboard,
    module.repo_frontend_app_publisher,
    module.repo_frontend_app_support_tools,
    module.repo_frontend_build,
    module.repo_frontend_component_cookie_policy_banner,
    module.repo_frontend_component_footer,
    module.repo_frontend_component_header,
    module.repo_frontend_enterprise,
    module.repo_frontend_learner_portal_base,
    module.repo_frontend_platform,
    module.repo_frontend_template_application,
    module.repo_help_tokens,
    module.repo_html_webpack_new_relic_plugin,
    module.repo_i18n_tools,
    module.repo_license_manager,
    module.repo_mdrst,
    module.repo_mockprock,
    module.repo_mongodbproxy,
    module.repo_opaque_keys,
    module.repo_open_edx_proposals,
    module.repo_openedx_calc,
    module.repo_openedx_census,
    module.repo_openedx_chem,
    module.repo_openedx_webhooks,
    module.repo_openedxstats,
    module.repo_paragon,
    module.repo_pytest_repo_health,
    module.repo_pytest_warnings_report,
    module.repo_ratexblock,
    module.repo_reactifex,
    module.repo_recommenderxblock,
    module.repo_registrar,
    module.repo_repo_tools,
    module.repo_repo_tools_data_schema,
    module.repo_sample_themes,
    module.repo_schoolyourself_xblock,
    module.repo_staff_graded_xblock,
    module.repo_studio_frontend,
    module.repo_stylelint_config_edx,
    module.repo_super_csv,
    module.repo_tincanpython,
    module.repo_tinymce_language_selector,
    module.repo_tubular,
    module.repo_user_util,
    module.repo_web_fragments,
    module.repo_xblock,
    module.repo_xblock_free_text_response,
    module.repo_xblock_image_modal,
    module.repo_xblock_in_video_quiz,
    module.repo_xblock_lti_consumer,
    module.repo_xblock_qualtrics_survey,
    module.repo_xblock_sdk,
    module.repo_xblock_sql_grader,
    module.repo_xblock_submit_and_compare,
    module.repo_xblock_utils,
    module.repo_xqueue,
    module.repo_xqueue_watcher,
    module.repo_xss_utils,
  ]
  users = [
    module.user_adamstankiewicz,
    module.user_adeelehsan,
    module.user_aghaawais01,
    module.user_ahernkb,
    module.user_ahsanshafiq742,
    module.user_aht007,
    module.user_ahtishamshahid,
    module.user_akummins,
    module.user_alangsto,
    module.user_albemarle,
    module.user_alex_sheehan_edx,
    module.user_alfredoguillem,
    module.user_ali_d_akbar,
    module.user_anhhhh,
    module.user_ansabgillani,
    module.user_antoviaque,
    module.user_arbabkhalil,
    module.user_arch_bom_gocd_alerts,
    module.user_ark_edly,
    module.user_asadazam93,
    module.user_ashultz0,
    module.user_attiyaishaque,
    module.user_awais_ansari,
    module.user_awais786,
    module.user_awaisdar001,
    module.user_azanbinzahid,
    module.user_bilalawan321,
    module.user_binodpant,
    module.user_bmedx,
    module.user_brianhw,
    module.user_bseverino,
    module.user_caplan188,
    module.user_carlos_muniz,
    module.user_ccarbs,
    module.user_ccmelo,
    module.user_cdeery,
    module.user_christopappas,
    module.user_ciduarte,
    module.user_colinbrash,
    module.user_connorhaugh,
    module.user_davidjoy,
    module.user_dawoudsheraz,
    module.user_debbiejacob,
    module.user_dianakhuang,
    module.user_dianekaplan,
    module.user_dillon_dumesnil,
    module.user_doctoryes,
    module.user_e0d,
    module.user_edx_build_docs_bot,
    module.user_edx_clamps,
    module.user_edx_codecov_bot,
    module.user_edx_requirements_bot,
    module.user_edx_semantic_release,
    module.user_edx_status_bot,
    module.user_ekangedx,
    module.user_enavarro,
    module.user_estute,
    module.user_farhan_arshad_dev,
    module.user_georgebabey,
    module.user_hammadahmadwaqas,
    module.user_hamzaisrar_arbisoft,
    module.user_hassanjaveed84,
    module.user_hbwhbw,
    module.user_hilaryg123,
    module.user_iamsobanjaved,
    module.user_iloveagent57,
    module.user_inventhouse,
    module.user_irfanuddinahmad,
    module.user_jansenk,
    module.user_jawad_khan,
    module.user_jawayria,
    module.user_jazibhumayun,
    module.user_jdmulloy,
    module.user_jinder1s,
    module.user_jjodonohue,
    module.user_jmbowman,
    module.user_jmyatt,
    module.user_jnlapierre,
    module.user_johnnagro,
    module.user_jpbeaudry,
    module.user_jristau1984,
    module.user_jsongedx,
    module.user_julianajlk,
    module.user_julieliberty,
    module.user_justinhynes,
    module.user_kafable,
    module.user_kashifch,
    module.user_kdmccormick,
    module.user_kenclary,
    module.user_kevincanavan,
    module.user_kiram15,
    module.user_leangseu_edx,
    module.user_llewenstein,
    module.user_long74100,
    module.user_loucicchese,
    module.user_macdiesel,
    module.user_manny_m,
    module.user_marcotuts,
    module.user_marekwrobel,
    module.user_mattcarter,
    module.user_mattdrayer,
    module.user_matthewpiatetsky,
    module.user_matthugs,
    module.user_mehaknasir,
    module.user_miankhalid,
    module.user_michaelroytman,
    module.user_mikix,
    module.user_moconnell1453,
    module.user_mondiaz,
    module.user_mraarif,
    module.user_mubbsharanwar,
    module.user_muhammad_ammar,
    module.user_mulby,
    module.user_mumer92,
    module.user_muneebgh,
    module.user_muselesscreator,
    module.user_nadeemshahzad,
    module.user_natabene,
    module.user_nedbat,
    module.user_nickett3,
    module.user_nickpizzo,
    module.user_nixknight,
    module.user_nrobertson1992,
    module.user_nsprenkle,
    module.user_oel8man,
    module.user_oliviaruizknott,
    module.user_omerhabib26,
    module.user_openedx_release_bot,
    module.user_ormsbee,
    module.user_pshiu,
    module.user_pwnage101,
    module.user_rgraber,
    module.user_robrap,
    module.user_saadyousafarbi,
    module.user_saeedbashir,
    module.user_saleem_latif,
    module.user_sameenfatima78,
    module.user_sapanathomas523,
    module.user_sarina,
    module.user_sbishop0905,
    module.user_schenedx,
    module.user_sethmccann,
    module.user_shafqatfarhan,
    module.user_spencertiberi,
    module.user_srwang,
    module.user_sstack22,
    module.user_syed_awais_ali,
    module.user_syedimranhassan,
    module.user_timmc_edx,
    module.user_tj_tracy,
    module.user_tuchfarber,
    module.user_usama101,
    module.user_usamasadiq,
    module.user_usmanmurad,
    module.user_uzairr,
    module.user_waheedahmed,
    module.user_wajeeha_khalid,
    module.user_wblarsen,
    module.user_wesmason,
    module.user_wittjeff,
    module.user_zacharis278,
    module.user_zainab_amir,
    module.user_zamanafzal,
  ]
}

module "role_edx_revenue_squad" {
  source = "./modules/role"
  admin_repos = [
    module.repo_ecommerce,
    module.repo_ecommerce_scripts,
    module.repo_ecommerce_worker,
    module.repo_frontend_app_ecommerce,
    module.repo_frontend_app_payment,
  ]
  users = [
    module.user_bmedx,
    module.user_colinbrash,
    module.user_dianekaplan,
    module.user_inventhouse,
    module.user_julianajlk,
    module.user_pshiu,
  ]
}

module "role_edx_semantic_release_bot" {
  source = "./modules/role"
  admin_repos = [
    module.repo_tinymce_language_selector,
  ]
  maintain_repos = [
    module.repo_taxonomy_connector,
  ]
  push_repos = [
    module.repo_edx_bootstrap,
    module.repo_frontend_app_enterprise_public_catalog,
    module.repo_frontend_app_gradebook,
    module.repo_frontend_app_learner_portal_enterprise,
    module.repo_frontend_app_program_console,
    module.repo_frontend_component_cookie_policy_banner,
    module.repo_frontend_enterprise,
    module.repo_frontend_learner_portal_base,
    module.repo_frontend_template_application,
    module.repo_studio_frontend,
  ]
  users = [
    module.user_edx_semantic_release,
  ]
}

module "role_edx_solutions_team" {
  source = "./modules/role"
  push_repos = [
    module.repo_sample_themes,
  ]
  users = [
    module.user_mattdrayer,
  ]
}

module "role_edx_sustaining_team" {
  source = "./modules/role"
  push_repos = [
    module.repo_openedx_webhooks,
    module.repo_xqueue,
  ]
  users = [
    module.user_kashifch,
  ]
}

module "role_edx_teaching_and_learning" {
  source = "./modules/role"
  admin_repos = [
    module.repo_blockstore,
    module.repo_brand_openedx,
    module.repo_ccx_keys,
    module.repo_cs_comments_service,
    module.repo_edx_platform,
    module.repo_edx_user_state_client,
    module.repo_frontend_app_learning,
    module.repo_frontend_app_library_authoring,
    module.repo_opaque_keys,
    module.repo_openedx_chem,
    module.repo_studio_frontend,
    module.repo_xblock,
    module.repo_xblock_sdk,
    module.repo_xblock_utils,
  ]
  push_repos = [
    module.repo_api_doc_tools,
    module.repo_frontend_app_course_authoring,
    module.repo_openedxstats,
  ]
  users = [
    module.user_connorhaugh,
    module.user_doctoryes,
    module.user_kdmccormick,
    module.user_kenclary,
    module.user_marcotuts,
    module.user_ormsbee,
  ]
}

module "role_edx_testeng" {
  source = "./modules/role"
  push_repos = [
    module.repo_django_config_models,
    module.repo_django_user_tasks,
    module.repo_edx_proctoring,
    module.repo_edx_sphinx_theme,
  ]
  users = [
    module.user_bilalawan321,
    module.user_estute,
    module.user_jmbowman,
  ]
}

module "role_edx_testeng_robot_rw" {
  source = "./modules/role"
  push_repos = [
    module.repo_api_doc_tools,
    module.repo_bok_choy,
    module.repo_codejail,
    module.repo_completion,
    module.repo_course_discovery,
    module.repo_credentials,
    module.repo_devstack,
    module.repo_django_config_models,
    module.repo_django_user_tasks,
    module.repo_ecommerce,
    module.repo_edx_analytics_dashboard,
    module.repo_edx_analytics_data_api,
    module.repo_edx_django_utils,
    module.repo_edx_enterprise,
    module.repo_edx_lint,
    module.repo_edx_organizations,
    module.repo_edx_platform,
    module.repo_edx_proctoring,
    module.repo_edx_rest_api_client,
    module.repo_edx_sphinx_theme,
    module.repo_edx_val,
    module.repo_openedxstats,
    module.repo_pytest_repo_health,
    module.repo_registrar,
    module.repo_studio_frontend,
    module.repo_xblock_utils,
    module.repo_xqueue,
    module.repo_xss_utils,
  ]
  users = [
    module.user_edx_requirements_bot,
    module.user_edx_status_bot,
  ]
}

module "role_edx_tools_core" {
  source = "./modules/role"
  admin_repos = [
    module.repo_edx_django_utils,
    module.repo_xss_utils,
  ]
  users = [
    module.user_estute,
    module.user_jmbowman,
  ]
}

module "role_edx_tools_edx_jenkins_pull_request_builder" {
  source = "./modules/role"
  push_repos = [
    module.repo_webhook_test_repo,
  ]
  users = [
    module.user_tools_edx_jenkins_pull_request_builder,
  ]
}

module "role_edx_transifex_translations" {
  source = "./modules/role"
  admin_repos = [
    module.repo_studio_frontend,
  ]
  push_repos = [
    module.repo_course_discovery,
    module.repo_credentials,
    module.repo_credentials_themes,
    module.repo_ecommerce,
    module.repo_edx_analytics_dashboard,
    module.repo_edx_django_utils,
    module.repo_edx_ora2,
    module.repo_edx_platform,
    module.repo_edx_proctoring,
    module.repo_xss_utils,
  ]
  users = [
    module.user_edx_transifex_bot,
  ]
}

module "role_edx_travis_admin" {
  source = "./modules/role"
  admin_repos = [
    module.repo_edx_app_android,
    module.repo_edx_app_ios,
    module.repo_edx_app_test,
    module.repo_edx_notes_api,
    module.repo_enmerkar_underscore,
    module.repo_frontend_app_publisher,
    module.repo_user_util,
  ]
  users = [
    module.user_adzuci,
    module.user_edx_travis_rw,
    module.user_feanil,
    module.user_timmc_edx,
  ]
}

module "role_edx_user_albemarle" {
  source = "./modules/role"
  admin_repos = [
    module.repo_frontend_app_support_tools,
  ]
  users = [
    module.user_albemarle,
  ]
}

module "role_edx_user_awaisdar001" {
  source = "./modules/role"
  admin_repos = [
    module.repo_docs_dot_edx_dot_org,
  ]
  users = [
    module.user_awaisdar001,
  ]
}

module "role_edx_user_bbrsofiane" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_frontend_platform,
  ]
  users = [
    module.user_bbrsofiane,
  ]
}

module "role_edx_user_carolguest" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_documentation,
  ]
  users = [
    module.user_carolguest,
  ]
}

module "role_edx_user_dawoudsheraz" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_analytics_configuration,
  ]
  users = [
    module.user_dawoudsheraz,
  ]
}

module "role_edx_user_dillon_dumesnil" {
  source = "./modules/role"
  admin_repos = [
    module.repo_frontend_app_publisher,
  ]
  users = [
    module.user_dillon_dumesnil,
  ]
}

module "role_edx_user_doctoryes" {
  source = "./modules/role"
  admin_repos = [
    module.repo_user_util,
  ]
  users = [
    module.user_doctoryes,
  ]
}

module "role_edx_user_edx_atlantis" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_edx_notes_api,
  ]
  users = [
    module.user_edx_atlantis,
  ]
}

module "role_edx_user_edx_deployment" {
  source = "./modules/role"
  admin_repos = [
    module.repo_edx_platform,
  ]
  push_repos = [
    module.repo_credentials,
    module.repo_credentials_themes,
  ]
  users = [
    module.user_edx_deployment,
  ]
}

module "role_edx_user_edx_revenue_tasks" {
  source = "./modules/role"
  admin_repos = [
    module.repo_ecommerce,
    module.repo_ecommerce_scripts,
    module.repo_ecommerce_worker,
    module.repo_frontend_app_ecommerce,
    module.repo_frontend_app_payment,
  ]
  users = [
    module.user_edx_revenue_tasks,
  ]
}

module "role_edx_user_edx_status_bot" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_app_android,
  ]
  users = [
    module.user_edx_status_bot,
  ]
}

module "role_edx_user_edx_transifex_bot" {
  source = "./modules/role"
  admin_repos = [
    module.repo_course_discovery,
    module.repo_ecommerce,
    module.repo_frontend_app_account,
    module.repo_frontend_app_authn,
    module.repo_frontend_app_course_authoring,
    module.repo_frontend_app_ecommerce,
    module.repo_frontend_app_learning,
    module.repo_frontend_app_payment,
    module.repo_frontend_app_profile,
    module.repo_frontend_component_footer,
  ]
  users = [
    module.user_edx_transifex_bot,
  ]
}

module "role_edx_user_edx_travis" {
  source = "./modules/role"
  admin_repos = [
    module.repo_api_doc_tools,
    module.repo_code_annotations,
    module.repo_completion,
    module.repo_crowdsourcehinter,
    module.repo_cypress_e2e_tests,
    module.repo_edx_celeryutils,
    module.repo_edx_cookiecutters,
    module.repo_edx_submissions,
    module.repo_edx_toggles,
    module.repo_edx_when,
    module.repo_enterprise_catalog,
    module.repo_eslint_config,
    module.repo_frontend_app_account,
    module.repo_frontend_app_authn,
    module.repo_frontend_app_ecommerce,
    module.repo_frontend_app_enterprise_public_catalog,
    module.repo_frontend_app_learner_portal_enterprise,
    module.repo_frontend_app_learner_portal_programs,
    module.repo_frontend_app_learning,
    module.repo_frontend_app_payment,
    module.repo_frontend_app_profile,
    module.repo_frontend_app_program_console,
    module.repo_frontend_app_publisher,
    module.repo_frontend_build,
    module.repo_frontend_component_cookie_policy_banner,
    module.repo_frontend_enterprise,
    module.repo_frontend_learner_portal_base,
    module.repo_frontend_platform,
    module.repo_license_manager,
    module.repo_openedx_calc,
    module.repo_registrar,
    module.repo_taxonomy_connector,
    module.repo_tincanpython,
    module.repo_tinymce_language_selector,
    module.repo_xblock_free_text_response,
    module.repo_xblock_image_modal,
    module.repo_xblock_in_video_quiz,
    module.repo_xblock_qualtrics_survey,
    module.repo_xblock_submit_and_compare,
    module.repo_xss_utils,
  ]
  push_repos = [
    module.repo_edx_analytics_exporter,
    module.repo_frontend_app_gradebook,
    module.repo_frontend_component_header,
  ]
  users = [
    module.user_edx_travis,
  ]
}

module "role_edx_user_georgebabey" {
  source = "./modules/role"
  admin_repos = [
    module.repo_taxonomy_connector,
  ]
  users = [
    module.user_georgebabey,
  ]
}

module "role_edx_user_iloveagent57" {
  source = "./modules/role"
  admin_repos = [
    module.repo_frontend_app_gradebook,
  ]
  users = [
    module.user_iloveagent57,
  ]
}

module "role_edx_user_jmyatt" {
  source = "./modules/role"
  admin_repos = [
    module.repo_frontend_app_publisher,
  ]
  users = [
    module.user_jmyatt,
  ]
}

module "role_edx_user_michellephilbrick" {
  source = "./modules/role"
  maintain_repos = [
    module.repo_open_edx_proposals,
  ]
  users = [
    module.user_michellephilbrick,
  ]
}

module "role_edx_user_mikix" {
  source = "./modules/role"
  admin_repos = [
    module.repo_frontend_app_publisher,
  ]
  users = [
    module.user_mikix,
  ]
}

module "role_edx_user_moconnell1453" {
  source = "./modules/role"
  admin_repos = [
    module.repo_taxonomy_connector,
  ]
  users = [
    module.user_moconnell1453,
  ]
}

module "role_edx_user_mslotkeedx" {
  source = "./modules/role"
  admin_repos = [
    module.repo_acclaimbadge_xblock,
  ]
  users = [
    module.user_mslotkeedx,
  ]
}

module "role_edx_user_precisionwordcraft" {
  source = "./modules/role"
  push_repos = [
    module.repo_edx_developer_docs,
  ]
  users = [
    module.user_precisionwordcraft,
  ]
}

module "role_edx_user_rgraber" {
  source = "./modules/role"
  push_repos = [
    module.repo_taxonomy_connector,
  ]
  users = [
    module.user_rgraber,
  ]
}

module "role_edx_user_schenedx" {
  source = "./modules/role"
  admin_repos = [
    module.repo_django_ratelimit_backend,
    module.repo_edx_analytics_dashboard,
    module.repo_edx_analytics_data_api,
    module.repo_frontend_app_gradebook,
  ]
  users = [
    module.user_schenedx,
  ]
}

module "role_edx_user_zacharis278" {
  source = "./modules/role"
  admin_repos = [
    module.repo_frontend_app_course_authoring,
  ]
  users = [
    module.user_zacharis278,
  ]
}

module "role_edx_ux_team" {
  source = "./modules/role"
  admin_repos = [
    module.repo_brand_openedx,
  ]
  users = [
    module.user_ekangedx,
  ]
}

module "role_edx_vanguards" {
  source = "./modules/role"
  admin_repos = [
    module.repo_frontend_app_authn,
  ]
  users = [
    module.user_adeelehsan,
    module.user_attiyaishaque,
    module.user_mubbsharanwar,
    module.user_shafqatfarhan,
    module.user_uzairr,
    module.user_waheedahmed,
    module.user_zainab_amir,
  ]
}

module "role_edx_webhook_admin" {
  source = "./modules/role"
  admin_repos = [
    module.repo_acid_block,
    module.repo_bok_choy,
    module.repo_codejail,
    module.repo_configuration,
    module.repo_cs_comments_service,
    module.repo_demo_performance_course,
    module.repo_django_lang_pref_middleware,
    module.repo_ease,
    module.repo_ecommerce,
    module.repo_ecommerce_worker,
    module.repo_edx_analytics_configuration,
    module.repo_edx_analytics_dashboard,
    module.repo_edx_analytics_data_api,
    module.repo_edx_analytics_data_api_client,
    module.repo_edx_app_android,
    module.repo_edx_app_gradle_plugin,
    module.repo_edx_app_ios,
    module.repo_edx_app_test,
    module.repo_edx_celeryutils,
    module.repo_edx_demo_course,
    module.repo_edx_django_utils,
    module.repo_edx_documentation,
    module.repo_edx_enterprise,
    module.repo_edx_enterprise_data,
    module.repo_edx_lint,
    module.repo_edx_milestones,
    module.repo_edx_notes_api,
    module.repo_edx_notifications,
    module.repo_edx_ora2,
    module.repo_edx_organizations,
    module.repo_edx_platform,
    module.repo_edx_proctoring,
    module.repo_edx_rest_api_client,
    module.repo_edx_search,
    module.repo_edx_submissions,
    module.repo_edx_tools,
    module.repo_edx_ui_toolkit,
    module.repo_edx_val,
    module.repo_event_tracking,
    module.repo_i18n_tools,
    module.repo_opaque_keys,
    module.repo_openedx_webhooks,
    module.repo_repo_tools,
    module.repo_stylelint_config_edx,
    module.repo_web_fragments,
    module.repo_xblock,
    module.repo_xblock_sdk,
    module.repo_xblock_utils,
    module.repo_xqueue,
    module.repo_xqueue_watcher,
    module.repo_xss_utils,
  ]
  users = [
    module.user_edx_webhook,
  ]
}

module "role_edx_website" {
  source = "./modules/role"
  admin_repos = [
    module.repo_frontend_component_cookie_policy_banner,
  ]
  users = [
    module.user_albemarle,
    module.user_kafable,
    module.user_marekwrobel,
    module.user_mulby,
    module.user_srwang,
  ]
}
