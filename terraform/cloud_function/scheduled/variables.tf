variable "attempt_deadline" {
  default = "320s"
}
variable "bucket_name" {}
variable "branch_suffix" {}
variable "function_env_vars" {}
variable "function_memory" {}
variable "function_name" {}
variable "iam_invoke_member" {}
variable "project_id" {}
variable "region" {}
variable "request_body" {
  default = "{}"
}
variable "request_method" {
  default = "POST"
}
variable "retry_count" {
  default = 1
}
variable "source_code_root_path" {}
variable "sa_email" {}
variable "schedule" {
  description = "See https://cloud.google.com/scheduler/docs/configuring/cron-job-schedules"
}
variable "timeout" { default = 60 }
variable "vpc_connector" {
  default = null
}
variable "vpc_connector_egress_settings" {
  default = null
}
