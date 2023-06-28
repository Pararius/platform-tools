data "google_bigquery_dataset" "fn" {
  dataset_id  = "fn"
  description = "Collection of standard and custom routines used across the platform"
  project     = local.google_project_id
  location    = local.region
}

resource "google_bigquery_routine" "greatest_non_null" {
  dataset_id      = data.google_bigquery_dataset.fn.dataset_id
  routine_id      = "greatest_non_null"
  routine_type    = "SCALAR_FUNCTION"
  language        = "SQL"
  definition_body = "(SELECT MAX(y) FROM UNNEST(x) AS y)"
  arguments {
    name          = "x"
    argument_kind = "ANY_TYPE"
  }
}
