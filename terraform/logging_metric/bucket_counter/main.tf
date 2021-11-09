resource "google_logging_metric" "default" {
  name   = format("%s%s", var.name, var.branch_suffix)
  filter        = <<EOT
resource.type="gcs_bucket"
resource.labels.bucket_name="${var.bucket_name}"
protoPayload.resourceName:"${var.prefix}uploads/"
protoPayload.methodName="${var.method}"
EOT
  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
  }
}
