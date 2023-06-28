resource "google_bigquery_routine" "greatest_non_null" {
  dataset_id      = "fn" # manually created dataset so have to hardcode (there is no data block for datasets yet, see: https://github.com/hashicorp/terraform-provider-google/issues/5693)
  definition_body = "(SELECT MAX(y) FROM UNNEST(x) AS y)"
  language        = "SQL"
  project         = local.google_project_id
  routine_id      = "greatest_non_null"
  routine_type    = "SCALAR_FUNCTION"

  arguments {
    name          = "x"
    argument_kind = "ANY_TYPE"
  }
}
