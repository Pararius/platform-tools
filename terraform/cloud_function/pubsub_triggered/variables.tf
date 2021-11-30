variable "bucket_name" {}
variable "branch_suffix" {}
variable "entry_point" {
  default = "handler"
}
variable "function_env_vars" {}
variable "function_memory" {}
variable "function_name" {}
variable "project_id" {}
variable "region" {}
variable "runtime" {
  default = "python39"
}
variable "sa_email" {}
variable "source_code_root_path" {}
variable "topic_id" {}
variable "timeout" { default = 60 }
