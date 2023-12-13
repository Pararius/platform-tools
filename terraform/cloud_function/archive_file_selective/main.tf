data "archive_file" "source" {
  type        = var.type
  output_path = format("/tmp/%s/archive.%s", var.name, var.type)

  dynamic "source" {
    for_each = var.files
    content {
      content  = file(abspath(source.value))
      filename = basename(source.value)
    }
  }
}
