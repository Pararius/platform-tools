variable "bucket_location" {
  type = string
}
variable "bucket_name" {
  type = string
}
variable "enable_versioning" {
  type    = bool
  default = true
}
variable "force_destroy" {
  type    = bool
  default = false
}
variable "labels" {
  type        = map(string)
  description = "Labels that should be passed to the Google Cloud resource"
  default     = {}
}
variable "lifecycle_rules" {
  type    = list(any)
  default = []
}
variable "storage_class" {
  type    = string
  default = "STANDARD"
}

