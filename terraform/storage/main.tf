resource "google_storage_bucket" "default" {
  name          = var.bucket_name
  location      = var.bucket_location
  storage_class = var.storage_class
  force_destroy = var.force_destroy

  versioning {
    enabled = var.enable_versioning
  }

  dynamic "lifecycle_rule" {
    for_each = var.lifecycle_rules

    content {
      action    = lifecycle_rule.value["action"]
      condition = lifecycle_rule.value["condition"]
    }
  }
}


