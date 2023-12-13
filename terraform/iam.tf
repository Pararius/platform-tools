// Generic SA for Cloud Functions
resource "google_service_account" "pt_cloud_function_runner" {
  project      = local.google_project_id
  account_id   = format("pt-cf-runner%s", substr(local.branch_suffix, 0, 30))
  display_name = "Schedules and runs all platform-tools pipelines${local.branch_suffix != "" ? format(" (suffix: %s)", local.branch_suffix) : ""}"
}

resource "google_project_iam_member" "cloud_function_runner_roles" {
  for_each = toset([
    "roles/cloudfunctions.invoker",
    "roles/iam.serviceAccountUser",
    "roles/secretmanager.secretAccessor",
    "roles/iam.serviceAccountTokenCreator",
  ])
  role    = each.key
  member  = "serviceAccount:${google_service_account.pt_cloud_function_runner.email}"
  project = local.google_project_id
}
