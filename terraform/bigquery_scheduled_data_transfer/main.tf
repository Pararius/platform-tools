locals {
  bigquery_cronjob_mappings = {
    "hourly" : "every hour",
    "daily" : "every day 00:00",
    "weekly" : "every monday 00:00",
    "quarterly" : "1 of jan,april,july,oct 00:00",
    "office hours" : "every hour from 06:00 to 15:00" # corrected for UTC (+2)
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
    query = templatefile(
      var.query_template,
      merge(var.query_variables, { interval = try(local.bigquery_interval_mappings[var.interval], var.interval) })
    )
    destination_table_name_template = var.destination_table_name_template
    write_disposition               = var.write_disposition
  }

  # formatting rules are quite hard to generalize, see: https://cloud.google.com/appengine/docs/flexible/scheduling-jobs-with-cron-yaml#cron_yaml_The_schedule_format
  schedule = try(local.bigquery_cronjob_mappings[var.interval], var.interval)

  schedule_options {
    disable_auto_scheduling = var.enable_auto_scheduling ? false : true
  }
}
