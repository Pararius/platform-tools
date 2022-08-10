output "artifacts_bucket_name" {
    value = module.platform-artifacts-bucket.bucket_name
}

output "platform_tools_artifact_prefix" {
    value = google_storage_bucket_object.platform-tools-artifact.name
}