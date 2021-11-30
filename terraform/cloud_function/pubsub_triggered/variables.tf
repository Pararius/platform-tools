variable "branch_suffix" {}
variable "function_entry_point" {
  default = "handler"
}
variable "function_env_vars" {
  default = {}
}
variable "function_memory" {
  default = 128
}
variable "function_name" {}
variable "function_runtime" {
  default = "python39"
}
variable "function_service_account_email" {}
variable "function_timeout" { default = 60 }
variable "project_id" {}
variable "project_region" {}
variable "pubsub_topic_id" {}
variable "source_code_bucket_name" {}
variable "source_code_root_path" {}
