/*
Cloud Function triggered by a message published on a PubSub topic.

Often used in conjunction with bucket notifications to act on newly created objects.
*/

locals {
  excluded_files = length(local.include_list) > 0 ? toset([
    for srcFile in local.source_files :
    srcFile if contains(local.include_list, srcFile) == false
  ]) : []
  include_list  = fileexists(abspath(format("%s/include.lst", local.source_prefix))) ? split("\n", file(format("%s/include.lst", local.source_prefix))) : []
  source_files  = fileset(local.source_prefix, "**")
  source_prefix = format("%s/%s", var.source_code_root_path, var.function_name)
}

# Compress source code
data "archive_file" "source" {
#  excludes    = local.excluded_files
  output_path = format("/tmp/%s/pubsub_function_%s.zip", var.function_name, formatdate("YYMMDDhhmmss", timestamp()))
  source_dir  = abspath(format("%s/%s", var.source_code_root_path, var.function_name))
  type        = "zip"
}

resource "google_storage_bucket_object" "functioncode" {
  name = format("pubsub_function_sources/%s/%s.zip", var.function_name, data.archive_file.source.output_md5)

  bucket = var.source_code_bucket_name
  source = data.archive_file.source.output_path
}

resource "google_cloudfunctions_function" "function" {
  name = format("%s%s", var.function_name, var.branch_suffix)

  available_memory_mb           = var.function_memory
  entry_point                   = var.function_entry_point
  environment_variables         = var.function_env_vars
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
