resource "google_monitoring_alert_policy" "pararius_legacy_data_alert_policy" {
  display_name = "${var.display_name} (branch suffix: ${var.branch_suffix})"
  combiner     = "OR"
  enabled      = var.enabled
  conditions {
    display_name = var.condition_display_name
    condition_threshold {
      filter          = "metric.type=\"logging.googleapis.com/user/${var.logging_metric_name}\" AND resource.type=\"gcs_bucket\""
      threshold_value = 1
      duration        = "0s"
      comparison      = "COMPARISON_LT"
      aggregations {
        alignment_period     = var.alignment_period
        cross_series_reducer = "REDUCE_NONE"
        per_series_aligner   = "ALIGN_DELTA"
      }
      trigger {
        count = 1
      }
    }
  }
  notification_channels = [var.notification_channel_name]
}