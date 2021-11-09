resource "google_storage_bucket" "default" {
  name          = var.bucket_name
  location      = var.bucket_location
  storage_class = var.storage_class
  force_destroy = var.force_destroy

  versioning {
    enabled = var.enable_versioning
  }
}


