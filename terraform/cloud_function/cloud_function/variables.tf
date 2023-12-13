variable "function_entry_point" {
  type        = string
  default     = "handler"
  description = "The name of the function that is called in your source code when the Cloud Function is triggered."
}
variable "function_env_vars" {
  type        = map(any)
  default     = {}
  description = "Environment variables that are passed to the Cloud Function and can be used to provide additional configuration."
}
variable "function_type" {
  type        = string
  default     = "http"
  description = "The type of Cloud Function used. Controls how the function is triggered. Can be either 'http' or 'pubsub'"
}
variable "function_min_instances" {
  type        = number
  default     = 0
  description = "The minimum number of Cloud Function instances that should be running at any time."
}
variable "function_max_instances" {
  type        = number
  default     = 1000
  description = "The maximum number of Cloud Function instances that should be running at any time."
}
variable "function_memory" {
  type        = number
  default     = 128
  description = "The amount of memory (in megabytes) that the Cloud Function instance is allowed to consume."
}
variable "function_name" {
  type        = string
  description = "A unique identity for this function, must be different than other functions you have in your project AND terraform workspaces (should include suffix!)."
}
variable "function_retry_on_failure" {
  type        = bool
  default     = false
  description = "Indicates whether the function should be retried on failure. Only applies when you expect your code to fail now and then."
}
variable "function_runtime" {
  type        = string
  default     = "python310"
  description = "The runtime used to execute your code, see https://cloud.google.com/functions/docs/runtime-support for more options."
}
variable "function_service_account_email" {
  type        = string
  description = "The email address of the service account used to run the Cloud Function instance. You should male sure it has all the roles necessary to run your code."
}
variable "function_timeout" {
  type        = number
  default     = 60
  description = "The maximum time in seconds to allow for this function to run. Can not be more than 540."
}
variable "function_vpc_connector" {
  type        = string
  default     = null
  description = "When provided, this allows the function to connect to the outside world through a specific VPC. Useful for connecting with systems that have an IP whitelist."
}
variable "function_vpc_connector_egress_settings" {
  type        = string
  default     = null
  description = "Restricts the kind of traffic allowed to pass through the VPC connector. Allowed values are ALL_TRAFFIC and PRIVATE_RANGES_ONLY. Defaults to PRIVATE_RANGES_ONLY. If unset, this field preserves the previously set value."
}
variable "google_cloud_project_id" {
  type        = string
  description = "The ID of the Google Cloud Project used to deploy this function."
}
variable "google_cloud_region" {
  type        = string
  description = "The region used to deploy this function on Google Cloud."
}
variable "scheduler_service_account_email" {
  type        = string
  default     = null
  description = "The email address of the service account used to schedule the Cloud Function instance (if configured to do so). You should make sure it has at least the `roles/cloudfunctions.invoker` role for it to work."
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
  description = "Specifies one or more intervals at which your Cloud Function should be triggered, and the request it should receive."
}
variable "source_code_bucket_name" {
  type        = string
  description = "The name of the bucket where source code for this function is stored."
}
variable "source_prefix" {
  type        = string
  default     = null
  description = "Points to the directory containing your function code. It should have at least a `main.py` file and an optional `requirements.txt` to install dependencies. Conflicts with `source_files`."
}
variable "source_files" {
  type        = list(string)
  default     = []
  description = "Points to specific files that make up your function. It can only point to a single `main.py` but more files can be added to extend functionality. Conflicts with `source_prefix`."
}
variable "pubsub_topic_id" {
  type        = string
  default     = null
  description = "The ID of the pubsub topic that this function should be triggered by (if any). Only works in conjunction with `type=pubsub`."
}
