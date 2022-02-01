variable "bucket_location" {}
variable "bucket_name" {}
variable "enable_versioning" {}
variable "force_destroy" {
  default = false
}
variable "lifecycle_rules" {
  default = []
}
variable "storage_class" {}

