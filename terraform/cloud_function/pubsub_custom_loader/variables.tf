variable "name" {
  type        = string
  description = "Name used to identify this collection of resources, automatically gets suffixed with `suffix` variable."
}

variable "google_cloud_project_id" {
  type        = string
  description = "The ID of the Google Cloud Project used to deploy this function."
}

variable "google_cloud_region" {
  type        = string
  description = "The region used to deploy this function on Google Cloud."
}

variable "pubsub_topic_id" {
  type        = string
  description = "The full PubSub topic ID that this loader should subscribe to (should start with projects/[project-id]/...)."
}

variable "service_account_email" {
  type        = string
  description = "The Service Account used to run (and optionally, schedule) the cloud functions needed for each step."
}

variable "source_code_bucket_name" {
  type        = string
  description = "The bucket used to store the source code needed to run a step."
}

variable "suffix" {
  type        = string
  description = "The suffix added to all resource names in order to differentiate environments (e.g. a feature branch or production) on Google Cloud."
}

variable "custom_source_code" {
  type        = string
  description = "Path to the directory that will be used as source code for the loading stage."
}

variable "custom_environment_variables" {
  type        = map(string)
  default     = {}
  description = "Variables that you would like to have available to your custom loader"
}
