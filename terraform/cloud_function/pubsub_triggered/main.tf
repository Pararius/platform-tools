/*
Cloud Function triggered by a message published on a PubSub topic.

Often used in conjunction with bucket notifications to act on objects created in a bucket.
*/
locals {
  timestamp = formatdate("YYMMDDhhmmss", timestamp())
  root_dir  = abspath(format("%s/%s", var.source_code_root_path, var.function_name))
}

# Compress source code
data "archive_file" "source" {
  type        = "zip"
  source_dir  = local.root_dir
  output_path = format("/tmp/pubsub_function_%s.zip", local.timestamp)
}

resource "google_storage_bucket_object" "functioncode" {
  name   = format("pubsub_function_sources/%s/sourcecode.zip#%s", var.function_name, data.archive_file.source.output_md5)
  bucket = var.source_code_bucket_name
  source = data.archive_file.source.output_path
}

resource "google_cloudfunctions_function" "function" {
  available_memory_mb           = var.function_memory
  entry_point                   = var.function_entry_point
  environment_variables         = var.function_env_vars
  name                          = format("%s%s", var.function_name, var.branch_suffix)
  project                       = var.project_id
  runtime                       = var.function_runtime
  service_account_email         = var.function_service_account_email
  source_archive_bucket         = google_storage_bucket_object.functioncode.bucket
  source_archive_object         = google_storage_bucket_object.functioncode.name
  timeout                       = var.function_timeout
  vpc_connector                 = var.function_vpc_connector
  vpc_connector_egress_settings = var.function_vpc_connector_egress_settings

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = var.pubsub_topic_id
  }
}