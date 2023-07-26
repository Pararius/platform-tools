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
  definition_body = "SAFE_CAST(JSON_VALUE(json_path) AS BOOL)"
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
  definition_body = "SAFE_CAST(JSON_VALUE(json_path) AS INT64)"
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

resource "google_bigquery_routine" "furnished_type_parser" {
  dataset_id   = local.routines_dataset
  routine_id   = "parse_furnished_type${local.branch_suffix_underscore_edition}"
  routine_type = "SCALAR_FUNCTION"
  language     = "JAVASCRIPT"
  arguments {
    name          = "raw_types"
    argument_kind = "FIXED_TYPE"
    data_type     = "{\"typeKind\": \"ARRAY<STRING>\"}"
  }
  definition_body = <<EOF
final_types = [];
raw_types = raw_types.map(raw_type => raw_type.toLowerCase());

if (raw_types.filter(t => t.includes("shell")) || raw_types.filter(t => t.includes("kaal"))) {
  final_types.push("shell");
}

if (raw_types.filter(t => t.includes("upholstered")) || raw_types.filter(t => t.includes("gestoffeerd"))) {
  final_types.push("upholstered");
}

if (raw_types.filter(t => t.includes("furnished")) || raw_types.filter(t => t.includes("gemeubileerd"))) {
  final_types.push("furnished");
}

return final_types;
EOF

  return_type = <<EOF
  {
  	"typeKind": "ARRAY<STRING>"
  }
EOF
}
