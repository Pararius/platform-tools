resource "google_logging_metric" "bucket_counter" {
  # Measures the number of times objects are created in a given bucket
  # Exact trigger (creation, modification, etc.) can be adjusted using the "method" variable.
  # This implementation was based on https://cloud.google.com/blog/products/storage-data-transfer/guide-to-setting-up-monitoring-for-object-creation-in-cloud-storage
  # and https://stackoverflow.com/a/37257217

  filter = <<EOT
resource.type="gcs_bucket"
resource.labels.bucket_name="${var.bucket_name}"
protoPayload.resourceName=~"^${var.prefix}"
protoPayload.methodName="${var.method}"
EOT
  name   = format("%s%s", var.name, var.branch_suffix)

  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
  }
}
