resource "google_pubsub_subscription" "custom_extractor" {
  name    = format("%s_custom_extractor%s", var.name, var.suffix)
  topic   = var.pubsub_topic_id
  project = var.google_cloud_project_id

  ack_deadline_seconds         = 150
  enable_exactly_once_delivery = false

  push_config {
    push_endpoint = module.custom_loader.https_trigger_url
    oidc_token {
      service_account_email = var.service_account_email
    }
  }

  retry_policy {
    minimum_backoff = "30s"
    maximum_backoff = "600s"
  }
}

module "custom_loader" {
  function_env_vars              = var.custom_environment_variables
  function_memory                = 512
  function_name                  = format("%s_custom_loader%s", var.name, var.suffix)
  function_service_account_email = var.service_account_email
  function_timeout               = 300
  function_type                  = "http"
  google_cloud_project_id        = var.google_cloud_project_id
  google_cloud_region            = var.google_cloud_region
  source                         = "./../cloud_function"
  source_code_bucket_name        = var.source_code_bucket_name
  source_prefix                  = var.custom_source_code
}
