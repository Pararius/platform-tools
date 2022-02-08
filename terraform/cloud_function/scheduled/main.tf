/*
Cloud Function invoked by a scheduled job through a HTTP request

Often used to do things that need to be executed at regular intervals,
like pulling data from external sources or doing (small) aggregations
*/

locals {
  excluded_files = length(local.include_list) > 0 ? toset([
    for srcFile in local.source_files :
    srcFile if contains(local.include_list, srcFile) == false
  ]) : []
  include_list  = fileexists(format("%s/include.lst", local.source_prefix)) ? split(file(format("%s/include.lst", local.source_prefix)), "\n") : []
  source_files  = fileset(path.module, format("%s/*.*", local.source_prefix))
  source_prefix = format("%s/%s", var.source_code_root_path, var.function_name)
}

# Compress source code
data "archive_file" "source" {
  excludes    = local.excluded_files
  output_path = format("/tmp/%s/http_function_%s.zip", var.function_name, formatdate("YYMMDDhhmmss", timestamp()))
  source_dir  = abspath(format("%s/%s", var.source_code_root_path, var.function_name))
  type        = "zip"
}

resource "google_storage_bucket_object" "functioncode" {
  name = format("http_function_sources/%s/%s.zip", var.function_name, data.archive_file.source.output_md5)

  bucket = var.source_code_bucket_name
  source = data.archive_file.source.output_path
}

resource "google_cloudfunctions_function" "function" {
  name = format("%s%s", var.function_name, var.branch_suffix)

  available_memory_mb           = var.function_memory
  entry_point                   = var.function_entry_point
  environment_variables         = var.function_env_vars
  project                       = var.project_id
  region                        = var.project_region
  runtime                       = var.function_runtime
  service_account_email         = var.function_service_account_email
  source_archive_bucket         = var.source_code_bucket_name
  source_archive_object         = google_storage_bucket_object.functioncode.name
  timeout                       = var.function_timeout
  trigger_http                  = true
  vpc_connector                 = var.function_vpc_connector
  vpc_connector_egress_settings = var.function_vpc_connector_egress_settings
}

resource "google_cloud_scheduler_job" "scheduler_job" {
  for_each = { for scheduler in var.schedulers : scheduler.name => scheduler }

  attempt_deadline = each.value.attempt_deadline != null ? each.value.attempt_deadline : "320s"
  name             = each.value.name
  schedule         = each.value.schedule
  time_zone        = "Europe/Amsterdam"

  retry_config {
    retry_count = each.value.retry_count != null ? each.value.retry_count : 1
  }

  http_target {
    body        = base64encode(each.value.request_body != null ? each.value.request_body : "{}")
    http_method = each.value.request_method != null ? each.value.request_method : "POST"

    headers = {
      "Content-Type" : "application/json"
    }

    uri = google_cloudfunctions_function.function.https_trigger_url

    oidc_token {
      service_account_email = var.scheduler_service_account_email
    }
  }
}

resource "google_cloudfunctions_function_iam_member" "invoker" {
  cloud_function = google_cloudfunctions_function.function.name
  member         = "serviceAccount:${var.scheduler_service_account_email}"
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  role           = "roles/cloudfunctions.invoker"
}
