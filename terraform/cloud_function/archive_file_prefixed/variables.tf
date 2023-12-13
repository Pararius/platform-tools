variable "name" {
  type        = string
  description = "A unique identity for this archived file"
}

variable "type" {
  type        = string
  default     = "zip"
  description = "The type of archive file to produce"
}

variable "prefix" {
  type        = string
  description = "The path to the directory containing all the files you want to archive. Nested directories are kept intact."
}
