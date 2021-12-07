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
variable "function_vpc_connector" {
  default = null
}
variable "function_vpc_connector_egress_settings" {
  default = null
}
variable "project_id" {}
variable "project_region" {}
variable "schedulers" {
  default = []
  type = list(object({
    attempt_deadline = optional(string)
    name = string
    schedule = string
    request_body = optional(string)
    request_method = optional(string)
    retry_count = optional(number)
    service_account_email = string
  }))
}
variable "source_code_bucket_name" {}
variable "source_code_root_path" {}
