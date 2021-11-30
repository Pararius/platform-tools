variable "bucket_name" {}
variable "branch_suffix" {}
variable "function_env_vars" {}
variable "function_memory" {}
variable "function_name" {}
variable "iam_invoke_member" {}
variable "project_id" {}
variable "region" {}
variable "source_code_root_path" {}
variable "cf_sa_account_email" {}
variable "timeout" { default = 60 }
variable "vpc_connector" {
  default = null
}
variable "vpc_connector_egress_settings" {
  default = null
}
