module "google_docs_access_checker" {
  function_env_vars = {

  }
  function_memory                 = 512
  function_name                   = "google-docs-access-checker${local.branch_suffix}"
  function_service_account_email  = google_service_account.pt_cloud_function_runner.email
  function_timeout                = 300
  function_type                   = "http"
  google_cloud_project_id         = local.google_project_id
  google_cloud_region             = local.region
  scheduler_service_account_email = google_service_account.pt_cloud_function_runner.email
  schedulers = var.git_branch == "" ? [
    {
      name     = "schedule-agent-huurwoningen-loader${local.branch_suffix}"
      schedule = "every week"
    }
  ] : []
  source                  = "./cloud_function/cloud_function"
  source_code_bucket_name = module.platform-artifacts-bucket.name
  source_prefix           = "./../tools/google-docs-access-checker"
}
