resource "google_storage_bucket_object" "functioncode" {
  bucket = var.bucket_name
  name   = format("function_sources/%s%s/source.zip", var.function_name, var.branch_suffix)
  source = var.path_to_zip_file
}

resource "google_cloudfunctions_function" "function" {
  available_memory_mb   = var.function_memory
  entry_point           = var.entry_point
  environment_variables = var.function_env_vars
  name                  = format("%s%s-%s", var.function_name, var.branch_suffix, substr(regex("(?:[a-zA-Z](?:[-_a-zA-Z0-9]{0,30}[a-zA-Z0-9])?)", google_storage_bucket_object.functioncode.md5hash), 0, 10)) # see https://github.com/hashicorp/terraform-provider-google/issues/1938#issuecomment-740532646
  project               = var.project_id
  runtime               = var.runtime
  service_account_email = google_service_account.cf_sa.email
  source_archive_bucket = google_storage_bucket_object.functioncode.bucket
  source_archive_object = google_storage_bucket_object.functioncode.name
  timeout               = var.timeout

  event_trigger {
    event_type = var.event_type
    resource   = var.topic_id
  }
}

resource "google_service_account" "cf_sa" {
  account_id   = format("gsa-%s", substr(md5(format("%s%s", var.function_name, var.branch_suffix)), 0, 26))
  display_name = "Service account for ${var.function_name} (branch suffix: ${var.branch_suffix})"
  project      = var.project_id
}

resource "google_project_iam_member" "cf_sa_pubsub" {
  member  = "serviceAccount:${google_service_account.cf_sa.email}"
  project = var.project_id
  role    = "roles/pubsub.publisher"
}

resource "google_project_iam_member" "cf_sa_user" {
  member  = "serviceAccount:${google_service_account.cf_sa.email}"
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
}
