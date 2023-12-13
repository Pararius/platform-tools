output "https_trigger_url" {
  value = var.function_type == "http" ? google_cloudfunctions_function.http_function[0].https_trigger_url : null
}

output "name" {
  value = var.function_type == "http" ? google_cloudfunctions_function.http_function[0].name : google_cloudfunctions_function.pubsub_function[0].name
}
