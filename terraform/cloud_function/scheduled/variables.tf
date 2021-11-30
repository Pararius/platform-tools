variable "attempt_deadline" {
  default = "320s"
}
variable "branch_suffix" {}
variable "bucket_name" {}
variable "entry_point" {
  default = "handler"
}
variable "function_env_vars" {}
variable "function_memory" {}
variable "function_name" {}
variable "iam_invoke_member_email" {}
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
variable "runtime" {
  default = "python39"
}
variable "sa_email" {}
variable "schedule" {
  description = "See https://cloud.google.com/scheduler/docs/configuring/cron-job-schedules"
}
variable "source_code_root_path" {}
variable "timeout" { default = 60 }
variable "vpc_connector" {
  default = null
}
variable "vpc_connector_egress_settings" {
  default = null
}
