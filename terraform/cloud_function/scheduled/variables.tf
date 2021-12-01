variable "branch_suffix" {}
variable "function_entry_point" {
  default = "handler"
}
variable "function_env_vars" {
  default = {}
}
variable "function_memory" {}
variable "function_name" {}
variable "function_project_id" {}
variable "function_project_region" {}
variable "function_runtime" {
  default = "python39"
}
variable "function_service_account_email" {}
variable "function_timeout" { default = 60 }
variable "function_vpc_connector" {
  default = null
}
variable "function_vpc_connector_egress_settings" {
  default = null
}
variable "scheduler_attempt_deadline" {
  default = "320s"
}
variable "scheduler_enabled" {
  default = 1
}
variable "scheduler_request_body" {
  default = "{}"
}
variable "scheduler_request_method" {
  default = "POST"
}
variable "scheduler_retry_count" {
  default = 1
}
variable "scheduler_schedule" {
  description = "See https://cloud.google.com/scheduler/docs/configuring/cron-job-schedules"
}
variable "scheduler_service_account_email" {}
variable "source_code_bucket_name" {}
variable "source_code_root_path" {}
