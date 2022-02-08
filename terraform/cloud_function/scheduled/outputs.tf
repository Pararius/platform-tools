output "https_trigger_url" {
  value = google_cloudfunctions_function.function.https_trigger_url
}

output "excluded_files" {
  value = join(",", local.excluded_files)
}

output "include_list" {
  value = join(",", local.include_list)
}
