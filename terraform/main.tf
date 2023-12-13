terraform {
  required_version = ">=1.3.0"
  backend "gcs" {
    bucket = "treehouse-dataplatform-tfstate"
    prefix = "platform-tools"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}


locals {
  branch_suffix_underscore_edition = var.git_branch == "" || var.git_branch == "main" ? "" : "_${replace(var.git_branch, "-", "_")}"
  branch_suffix                    = var.git_branch == "" || var.git_branch == "main" ? "" : "-${var.git_branch}"
  data_source_branch_suffix        = ""
  is_production                    = var.git_branch == "" || contains([], var.git_branch)
  google_project_id                = "data-prod-123456"
  region                           = "europe-west1"
  zone                             = "europe-west1-b"

  routines_dataset = "fn" # manually created dataset so have to hardcode (there is no data block for datasets yet, see: https://github.com/hashicorp/terraform-provider-google/issues/5693)
}

module "platform-artifacts-bucket" {
  source = "github.com/Pararius/platform-tools//terraform/storage"

  bucket_name       = "treehouse-dataplatform-artifacts${local.branch_suffix}"
  bucket_location   = local.region
  storage_class     = "STANDARD"
  enable_versioning = true
  force_destroy     = local.is_production ? false : true
}

module "platform-tools-source-code" {
  source = "github.com/Pararius/platform-tools//terraform/storage"

  bucket_name       = "treehouse-dataplatform-platform-tools-source-code${local.branch_suffix}"
  bucket_location   = local.region
  storage_class     = "STANDARD"
  enable_versioning = true
  force_destroy     = local.is_production ? false : true
}
