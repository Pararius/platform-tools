resource "google_logging_metric" "default" {
  name   = format("%s%s", var.name, var.branch_suffix)
  filter = var.filter # e.g. "resource.type=gae_app AND severity>=ERROR"
  metric_descriptor {
    metric_kind = var.metric_kind
    value_type  = var.metric_value_type
  }
}
