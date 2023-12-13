variable "name" {
  type        = string
  description = "A unique identity for this archived file"
}

variable "type" {
  type        = string
  default     = "zip"
  description = "The type of archive file to produce"
}

variable "files" {
  type        = list(string)
  description = "A list of (relative or absolute) paths to the files you want to include in the archive."
}
