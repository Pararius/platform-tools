locals {
  bigquery_cronjob_mappings = {
    "hourly" : "every hour",
    "daily" : "every day 00:00",
    "weekly" : "every monday 00:00",
    "quarterly" : "1 of jan,april,july,oct 00:00",
    # corrected for UTC -> Europe/Amsterdam including DST (+1 or +2), unfortunately the format does not seem to support combining hour ranges with day ranges
    "office hours" : "every hour from 06:00 to 16:00"
  }
  bigquery_interval_mappings = {
    "hourly" : "1 HOUR",
    "daily" : "1 DAY",
    "weekly" : "1 WEEK",
    "quarterly" : "1 QUARTER"
  }
}

resource "google_bigquery_data_transfer_config" "default" {
  data_source_id = "scheduled_query"
  display_name   = var.name
  location       = var.location

  destination_dataset_id = var.destination_dataset_id

  params = {
    destination_table_name_template = var.destination_table_name_template
    query = templatefile(
      "./scheduled_query_with_labels.sql",
      {
        LABELS_STRING = join("\n", [for key, value in var.labels : format("SET @@query_label = \"%s:%s\";", key, value)])
        ORIGINAL_QUERY = templatefile(
          var.query_template,
          merge(var.query_variables, { interval = try(local.bigquery_interval_mappings[var.interval], var.interval) })
        )
      }
    )
    write_disposition = var.write_disposition
  }

  # formatting rules are quite hard to generalize, see: https://cloud.google.com/appengine/docs/flexible/scheduling-jobs-with-cron-yaml#cron_yaml_The_schedule_format
  schedule = try(local.bigquery_cronjob_mappings[var.interval], var.interval)

  service_account_name = var.service_account_email

  schedule_options {
    disable_auto_scheduling = var.enable_auto_scheduling ? false : true
  }
}
