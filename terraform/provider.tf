provider "google" {
  project = local.google_project_id
  region  = local.region
  zone    = local.zone
}