resource "google_storage_bucket_object" "functioncode" {
  name   = "function_sources/${var.function_name}${var.branch_suffix}/source.zip"
  bucket = var.bucket_name
  source = var.path_to_zip_file
}

resource "google_cloudfunctions_function" "function" {
  project = var.project_id
  # see https://github.com/hashicorp/terraform-provider-google/issues/1938#issuecomment-740532646
  name = format("%s%s-%s", var.function_name, var.branch_suffix, substr(regex("(?:[a-zA-Z](?:[-_a-zA-Z0-9]{0,30}[a-zA-Z0-9])?)",
  google_storage_bucket_object.functioncode.md5hash), 0, 10))
  runtime = "python39"

  available_memory_mb   = var.function_memory
  source_archive_bucket = google_storage_bucket_object.functioncode.bucket
  source_archive_object = google_storage_bucket_object.functioncode.name
  entry_point           = "handler"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = var.topic_id
  }

  service_account_email = google_service_account.cf_sa.email
  environment_variables = var.function_env_vars
  timeout               = var.timeout
}

resource "google_service_account" "cf_sa" {
  project      = var.project_id
  account_id   = format("gsa-%s", substr(md5(format("%s%s", var.function_name, var.branch_suffix)), 0, 26))
  display_name = "Service account for ${var.function_name} (branch suffix: ${var.branch_suffix})"
}
