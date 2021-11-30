/*
Cloud Function invoked by a scheduled job through a HTTP request

Often used to do things that need to be executed at regular intervals,
like pulling data from external sources or doing aggregations
*/

resource "random_string" "random" {
  length           = 16
  special          = true
  override_special = "/@£$"
}

resource "google_storage_bucket_object" "functioncode" {
  name   = format("http_function_sources/%s/sourcecode%s.zip", var.function_name, random_string.random.result)
  bucket = var.source_code_bucket_name
  source = "${var.source_code_root_path}/${var.function_name}/${var.function_name}.zip"
}

resource "google_cloudfunctions_function" "function" {
  available_memory_mb           = var.function_memory
  entry_point                   = var.function_entry_point
  environment_variables         = var.function_env_vars
  name                          = format("%s%s", var.function_name, var.branch_suffix)
  project                       = var.project_id
  region                        = var.project_region
  runtime                       = var.function_runtime
  service_account_email         = var.function_service_account_email
  source_archive_bucket         = var.source_code_bucket_name
  source_archive_object         = google_storage_bucket_object.functioncode.name
  timeout                       = var.function_timeout
  trigger_http                  = true
  vpc_connector                 = var.vpc_connector
  vpc_connector_egress_settings = var.vpc_connector_egress_settings
}

# Add cloud scheduler job
resource "google_cloud_scheduler_job" "casco_listing_job" {
  count    = var.branch_suffix == "" ? 1 : 0 # Only enable job on production to avoid branches eating each others lunch
  name     = format("%s%s", var.function_name, substr(md5(var.branch_suffix), 0, 26))
  schedule = var.schedule

  time_zone        = "Europe/Amsterdam"
  attempt_deadline = var.attempt_deadline

  retry_config {
    retry_count = var.retry_count
  }

  http_target {
    http_method = var.request_method
    uri         = google_cloudfunctions_function.function.https_trigger_url
    body        = base64encode(var.request_body)

    oidc_token {
      service_account_email = var.iam_invoke_member_email
    }
  }
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = "serviceAccount:${var.iam_invoke_member_email}"
}
