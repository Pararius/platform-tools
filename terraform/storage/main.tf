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
    iterator = rule
    content {

      dynamic "action" {
        for_each = lookup(rule.value, "action", [])
        iterator = action

        content {
          type          = action.value.type
          storage_class = lookup(action.value, "storage_class", null)
        }
      }

      dynamic "condition" {
        for_each = lookup(rule.value, "condition", [])
        iterator = condition

        content {
          age = lookup(condition.value, "age", null)
        }
      }
    }
  }
}


