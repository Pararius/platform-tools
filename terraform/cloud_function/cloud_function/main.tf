module "archive_selective" {
  count  = length(var.source_files) > 0 ? 1 : 0
  source = "./../archive_file_selective"
  files  = var.source_files
  name   = var.function_name
}

module "archive_prefixed" {
  count  = length(var.source_files) == 0 ? 1 : 0
  source = "./../archive_file_prefixed"
  prefix = var.source_prefix
  name   = var.function_name
}

resource "google_storage_bucket_object" "function_source_code" {
  name = format("function_source_code/%s/%s.zip", var.function_name, length(var.source_files) > 0 ? module.archive_selective[0].output_md5 : module.archive_prefixed[0].output_md5)

  bucket = var.source_code_bucket_name
  source = length(var.source_files) > 0 ? module.archive_selective[0].output_path : module.archive_prefixed[0].output_path
}

resource "google_cloudfunctions_function" "http_function" {
  count                         = var.function_type == "http" ? 1 : 0
  name                          = var.function_name
  available_memory_mb           = var.function_memory
  entry_point                   = var.function_entry_point
  environment_variables         = var.function_env_vars
  project                       = var.google_cloud_project_id
  region                        = var.google_cloud_region
  runtime                       = var.function_runtime
  service_account_email         = var.function_service_account_email
  source_archive_bucket         = google_storage_bucket_object.function_source_code.bucket
  source_archive_object         = google_storage_bucket_object.function_source_code.name
  timeout                       = var.function_timeout
  trigger_http                  = true
  vpc_connector                 = var.function_vpc_connector
  vpc_connector_egress_settings = var.function_vpc_connector_egress_settings
  max_instances                 = var.function_max_instances
  min_instances                 = var.function_min_instances

  timeouts {
    create = "10m"
    update = "10m"
  }
}

resource "google_cloudfunctions_function" "pubsub_function" {
  count                         = var.function_type == "pubsub" ? 1 : 0
  name                          = var.function_name
  available_memory_mb           = var.function_memory
  entry_point                   = var.function_entry_point
  environment_variables         = var.function_env_vars
  project                       = var.google_cloud_project_id
  region                        = var.google_cloud_region
  runtime                       = var.function_runtime
  service_account_email         = var.function_service_account_email
  source_archive_bucket         = google_storage_bucket_object.function_source_code.bucket
  source_archive_object         = google_storage_bucket_object.function_source_code.name
  timeout                       = var.function_timeout
  vpc_connector                 = var.function_vpc_connector
  vpc_connector_egress_settings = var.function_vpc_connector_egress_settings
  max_instances                 = var.function_max_instances
  min_instances                 = var.function_min_instances

  timeouts {
    create = "10m"
    update = "10m"
  }

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = var.pubsub_topic_id
    failure_policy {
      retry = var.function_retry_on_failure
    }
  }
}

resource "google_cloud_scheduler_job" "scheduler_job" {
  for_each = { for scheduler in var.schedulers : scheduler.name => scheduler if var.function_type == "http" }

  attempt_deadline = each.value.attempt_deadline != null ? each.value.attempt_deadline : "320s"
  name             = each.value.name
  schedule         = each.value.schedule
  time_zone        = "UTC"
  project          = var.google_cloud_project_id
  region           = var.google_cloud_region

  retry_config {
    retry_count = each.value.retry_count != null ? each.value.retry_count : 1
  }

  http_target {
    body        = base64encode(each.value.request_body != null ? each.value.request_body : "{}")
    http_method = each.value.request_method != null ? each.value.request_method : "POST"

    headers = {
      "Content-Type" : "application/json"
    }

    uri = google_cloudfunctions_function.http_function[0].https_trigger_url

    oidc_token {
      service_account_email = var.scheduler_service_account_email
    }
  }
}
