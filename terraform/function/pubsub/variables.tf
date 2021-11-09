variable "branch_suffix" {}
variable "bucket_name" {}
variable "entry_point" {
  default = "handler"
}
variable "event_type" {
  default = "google.pubsub.topic.publish"
}
variable "function_env_vars" {}
variable "function_memory" {
  default = 128
}
variable "function_name" {}
variable "path_to_zip_file" {}
variable "project_id" {}
variable "region" {}
variable "runtime" {
  default = "python39"
}
variable "topic_id" {}
variable "timeout" { default = 60 }
