resource "google_storage_bucket_object" "platform-tools-artifact" {
  name = format("platform_tools/%s/%s", local.branch_suffix == "" ? "latest" : var.git_branch, var.platform_tools_artifact_filename)

  bucket = module.platform-artifacts-bucket.bucket_name
  source = format("../%s", var.platform_tools_artifact_filename)
}
