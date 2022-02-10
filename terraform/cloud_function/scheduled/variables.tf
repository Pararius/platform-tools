# must be defined in same file as where we define the variable with optional attrs
terraform {
  experiments = [module_variable_optional_attrs]
}

variable "branch_suffix" {
  type = string
}
variable "function_entry_point" {
  type    = string
  default = "handler"
}
variable "function_env_vars" {
  type    = map(any)
  default = {}
}
variable "function_memory" {
  type    = number
  default = 128
}
variable "function_name" {
  type = string
}
variable "function_name_prefix" {
  type    = string
  default = ""
}
variable "function_runtime" {
  type    = string
  default = "python39"
}
variable "function_service_account_email" {
  type = string
}
variable "function_timeout" {
  type    = number
  default = 60
}
variable "function_vpc_connector" {
  type    = string
  default = null
}
variable "function_vpc_connector_egress_settings" {
  type    = string
  default = null
}
variable "project_id" {
  type = string
}
variable "project_region" {
  type = string
}
variable "scheduler_service_account_email" {
  type = string
}
variable "schedulers" {
  default = []
  type = list(object({
    attempt_deadline = optional(string)
    name             = string
    schedule         = string
    request_body     = optional(string)
    request_method   = optional(string)
    retry_count      = optional(number)
  }))
}
variable "source_code_bucket_name" {
  type = string
}
variable "source_code_root_path" {
  type = string
}
