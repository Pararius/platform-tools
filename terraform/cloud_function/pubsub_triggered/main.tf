/*
Cloud Function triggered by a message published on a PubSub topic.
Often used in conjunction with bucket notifications to act on objects created in a bucket.
*/

resource "random_string" "random" {
  length           = 16
  special          = true
  override_special = "/@£$"
}

resource "google_storage_bucket_object" "functioncode" {
  name   = format("pubsub_function_sources/%s/sourcecode%s.zip", var.function_name, random_string.random.result)
  bucket = var.bucket_name
  source = format("%s/%s/%s.zip", var.source_code_root_path, var.function_name, var.function_name)
}

resource "google_cloudfunctions_function" "function" {
  project = var.project_id
  name    = format("%s%s", var.function_name, var.branch_suffix)
  runtime = var.runtime

  available_memory_mb   = var.function_memory
  source_archive_bucket = google_storage_bucket_object.functioncode.bucket
  source_archive_object = google_storage_bucket_object.functioncode.name
  entry_point           = var.entry_point

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = var.topic_id
  }

  service_account_email = var.sa_email
  environment_variables = var.function_env_vars
  timeout               = var.timeout
}
