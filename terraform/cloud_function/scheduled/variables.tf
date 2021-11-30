variable "attempt_deadline" {
  default = "320s"
}
variable "branch_suffix" {}
variable "function_entry_point" {
  default = "handler"
}
variable "function_env_vars" {
  default = {}
}
variable "function_memory" {}
variable "function_name" {}
variable "function_runtime" {
  default = "python39"
}
variable "function_service_account_email" {}
variable "function_timeout" { default = 60 }
variable "iam_invoke_member_email" {}
variable "project_id" {}
variable "project_region" {}
variable "request_body" {
  default = "{}"
}
variable "request_method" {
  default = "POST"
}
variable "retry_count" {
  default = 1
}
variable "schedule" {
  description = "See https://cloud.google.com/scheduler/docs/configuring/cron-job-schedules"
}
variable "source_code_bucket_name" {}
variable "source_code_root_path" {}
variable "vpc_connector" {
  default = null
}
variable "vpc_connector_egress_settings" {
  default = null
}
