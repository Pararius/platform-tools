resource "google_bigquery_routine" "empty_to_null" {
  dataset_id      = local.routines_dataset
  definition_body = "IF(LOWER(TRIM(SAFE_CAST(x AS STRING))) IN ('none', 'null', 'nan', 'nat', ''), NULL, x)"
  language        = "SQL"
  project         = local.google_project_id
  routine_id      = "empty_to_null${local.branch_suffix_underscore_edition}"
  routine_type    = "SCALAR_FUNCTION"

  arguments {
    name          = "x"
    argument_kind = "ANY_TYPE"
  }
}

resource "google_bigquery_routine" "greatest_non_null" {
  dataset_id      = local.routines_dataset
  definition_body = "(SELECT MAX(y) FROM UNNEST(x) AS y)"
  language        = "SQL"
  project         = local.google_project_id
  routine_id      = "greatest_non_null${local.branch_suffix_underscore_edition}"
  routine_type    = "SCALAR_FUNCTION"

  arguments {
    name          = "x"
    argument_kind = "ANY_TYPE"
  }
}

resource "google_bigquery_routine" "json_get_string" {
  dataset_id      = local.routines_dataset
  definition_body = "SAFE_CAST(JSON_VALUE(json_path) AS STRING)"
  language        = "SQL"
  project         = local.google_project_id
  routine_id      = "json_string${local.branch_suffix_underscore_edition}"
  routine_type    = "SCALAR_FUNCTION"

  arguments {
    name          = "json_path"
    argument_kind = "ANY_TYPE"
  }

  return_type = "{\"typeKind\" :  \"STRING\"}"
}

resource "google_bigquery_routine" "json_get_timestamp" {
  dataset_id      = local.routines_dataset
  definition_body = "SAFE_CAST(JSON_VALUE(json_path) AS TIMESTAMP)"
  language        = "SQL"
  project         = local.google_project_id
  routine_id      = "json_timestamp${local.branch_suffix_underscore_edition}"
  routine_type    = "SCALAR_FUNCTION"

  arguments {
    name          = "json_path"
    argument_kind = "ANY_TYPE"
  }

  return_type = "{\"typeKind\" :  \"TIMESTAMP\"}"
}

resource "google_bigquery_routine" "json_get_bool" {
  dataset_id      = local.routines_dataset
  definition_body = <<EOF
IF(
  LOWER(SAFE_CAST(JSON_VALUE(json_path) AS STRING)) IN ("ja", "yes", "true", "1", "1.0"),
  TRUE,
  IF(
    LOWER(SAFE_CAST(JSON_VALUE(json_path) AS STRING)) IN ("nee", "no", "false", "0", "0.0"),
    FALSE,
    SAFE_CAST(JSON_VALUE(json_path) AS BOOL)
  )
)
EOF
  language        = "SQL"
  project         = local.google_project_id
  routine_id      = "json_bool${local.branch_suffix_underscore_edition}"
  routine_type    = "SCALAR_FUNCTION"

  arguments {
    name          = "json_path"
    argument_kind = "ANY_TYPE"
  }

  return_type = "{\"typeKind\" :  \"BOOL\"}"
}

resource "google_bigquery_routine" "json_get_int" {
  dataset_id      = local.routines_dataset
  definition_body = "SAFE_CAST(SAFE_CAST(JSON_VALUE(json_path) AS NUMERIC) AS INT64)"
  language        = "SQL"
  project         = local.google_project_id
  routine_id      = "json_int${local.branch_suffix_underscore_edition}"
  routine_type    = "SCALAR_FUNCTION"

  arguments {
    name          = "json_path"
    argument_kind = "ANY_TYPE"
  }

  return_type = "{\"typeKind\" :  \"INT64\"}"
}

resource "google_bigquery_routine" "json_get_float" {
  dataset_id      = local.routines_dataset
  definition_body = "SAFE_CAST(JSON_VALUE(json_path) AS FLOAT64)"
  language        = "SQL"
  project         = local.google_project_id
  routine_id      = "json_float${local.branch_suffix_underscore_edition}"
  routine_type    = "SCALAR_FUNCTION"

  arguments {
    name          = "json_path"
    argument_kind = "ANY_TYPE"
  }

  return_type = "{\"typeKind\" :  \"FLOAT64\"}"
}


resource "google_storage_bucket_object" "user_agent_parser_lib" {
  name = "bigquery_functions/user_agent_parser/woothee.js"

  bucket = module.platform-artifacts-bucket.bucket_name
  source = "./woothee.js"
}

resource "google_bigquery_routine" "user_agent_parser" {
  dataset_id   = local.routines_dataset
  routine_id   = "user_agent_parser${local.branch_suffix_underscore_edition}"
  routine_type = "SCALAR_FUNCTION"
  language     = "JAVASCRIPT"
  imported_libraries = [
    format("gs://%s/%s", google_storage_bucket_object.user_agent_parser_lib.bucket, google_storage_bucket_object.user_agent_parser_lib.name)
  ]
  arguments {
    name      = "ua"
    data_type = "{\"typeKind\" :  \"STRING\"}"
  }
  definition_body = "return {category: woothee.parse(ua).category, name: woothee.parse(ua).name, version: woothee.parse(ua).version, os: woothee.parse(ua).os, vendor: woothee.parse(ua).vendor, os_version: woothee.parse(ua).os_version};"

  return_type = <<EOF
  {
  	"typeKind": "STRUCT",
  	"structType": {
  		"fields": [{
  				"name": "category",
  				"type": {
  					"typeKind": "STRING"
  				}
  			},
  			{
  				"name": "name",
  				"type": {
  					"typeKind": "STRING"
  				}
  			},
  			{
  				"name": "version",
  				"type": {
  					"typeKind": "STRING"
  				}
  			},
  			{
  				"name": "os",
  				"type": {
  					"typeKind": "STRING"
  				}
  			},
  			{
  				"name": "vendor",
  				"type": {
  					"typeKind": "STRING"
  				}
  			},
  			{
  				"name": "os_version",
  				"type": {
  					"typeKind": "STRING"
  				}
  			}
  		]
  	}
  }
EOF
}

resource "google_bigquery_routine" "greatest_furnished_type" {
  dataset_id   = local.routines_dataset
  routine_id   = "greatest_furnished_type${local.branch_suffix_underscore_edition}"
  routine_type = "SCALAR_FUNCTION"
  arguments {
    name          = "raw_types"
    argument_kind = "FIXED_TYPE"
    data_type     = "{\"typeKind\": \"ARRAY\", \"arrayElementType\": {\"typeKind\": \"STRING\"}}"
  }
  definition_body = <<EOF
IF(
  REGEXP_CONTAINS(ARRAY_TO_STRING(raw_types, ','), 'furnished|gemeubileerd'),
  'furnished',
  IF(
    REGEXP_CONTAINS(ARRAY_TO_STRING(raw_types, ','), 'upholstered|gestoffeerd'),
    'upholstered',
    IF(
      REGEXP_CONTAINS(ARRAY_TO_STRING(raw_types, ','), 'shell|kaal'),
      'shell',
      NULL
    )
  )
)
EOF
  language        = "SQL"
  return_type     = "{\"typeKind\": \"STRING\"}"
}

resource "google_bigquery_routine" "parse_dutch_date" {
  dataset_id   = local.routines_dataset
  project      = local.google_project_id
  routine_id   = "parse_dutch_date${local.branch_suffix_underscore_edition}"
  routine_type = "SCALAR_FUNCTION"

  arguments {
    name          = "date_str"
    argument_kind = "FIXED_TYPE"
    data_type     = "{\"typeKind\" :  \"STRING\"}"
  }

  language    = "SQL"
  return_type = "{\"typeKind\": \"STRING\"}"

  definition_body = <<EOF
  CAST(PARSE_DATE(
    "%F",
    CONCAT(
    SPLIT(date_str,' ')[OFFSET(2)],
    "-",
    CASE LOWER(SPLIT(date_str,' ')[OFFSET(1)])
      WHEN "januari" THEN "01"
      WHEN "februari" THEN "02"
      WHEN "maart" THEN "03"
      WHEN "april" THEN "04"
      WHEN "mei" THEN "05"
      WHEN "juni" THEN "06"
      WHEN "juli" THEN "07"
      WHEN "augustus" THEN "08"
      WHEN "september" THEN "09"
      WHEN "oktober" THEN "10"
      WHEN "november" THEN "11"
      WHEN "december" THEN "12"
    END,
    "-",
    SPLIT(date_str,' ')[OFFSET(0)])
  ) AS STRING)
EOF
}

resource "google_bigquery_routine" "query_string_to_json" {
  dataset_id   = local.routines_dataset
  routine_id   = "query_string_to_json${local.branch_suffix_underscore_edition}"
  routine_type = "SCALAR_FUNCTION"
  language     = "JAVASCRIPT"
  arguments {
    name      = "qs"
    data_type = "{\"typeKind\" :  \"STRING\"}"
  }
  definition_body = <<EOF
if (qs.charAt(0) == '?') {
  qs = qs.substring(1)
}

return JSON.stringify(JSON.parse('{"' + decodeURI(qs.replace(/&/g, "\",\"").replace(/=/g,"\":\"")) + '"}'))
EOF

  return_type = "{\"typeKind\": \"STRING\"}"
}
