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
variable "function_min_instances" {
  type    = number
  default = 0
}
variable "function_max_instances" {
  type    = number
  default = 1000
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
variable "function_retry_on_failure" {
  type    = bool
  default = false
}
variable "function_runtime" {
  type    = string
  default = "python310"
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

variable "labels" {
  default     = {}
  description = "Labels that should be passed to the Google Cloud resource"
  type        = map(string)
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
