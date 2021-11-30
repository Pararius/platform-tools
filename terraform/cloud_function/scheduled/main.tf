resource "random_string" "random" {
  length           = 16
  special          = true
  override_special = "/@£$"
}

resource "google_storage_bucket_object" "functioncode" {
  name   = format("http_function_sources/%s/sourcecode%s.zip", var.function_name, random_string.random.result)
  bucket = var.bucket_name
  source = "${var.source_code_root_path}/${var.function_name}/${var.function_name}.zip"
}

resource "google_cloudfunctions_function" "function" {
  project = var.project_id
  name    = format("%s%s", var.function_name, var.branch_suffix)
  runtime = "python39"
  region  = var.region

  available_memory_mb   = var.function_memory
  source_archive_bucket = var.bucket_name
  source_archive_object = google_storage_bucket_object.functioncode.name
  trigger_http          = true
  entry_point           = "handler"

  service_account_email         = var.cf_sa_account_email
  environment_variables         = var.function_env_vars
  vpc_connector                 = var.vpc_connector
  vpc_connector_egress_settings = var.vpc_connector_egress_settings

  timeout = var.timeout
}

# Add cloud scheduler job
resource "google_cloud_scheduler_job" "casco_listing_job" {
  count = var.branch_suffix == "" ? 1 : 0
  #Only enable job on production to avoid branches eating each others lunch
  name        = "casco-listing-job${substr(md5("${var.branch_suffix}"), 0, 26)}"
  description = "job to pull casco listings from topic"

  schedule = "*/15 * * * *"

  time_zone        = "Europe/Amsterdam"
  attempt_deadline = "320s"

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = module.casco_listing_cf.https_trigger_url
    body        = base64encode("{}")

    oidc_token {
      service_account_email = google_service_account.cs_sa.email
    }
  }
}
