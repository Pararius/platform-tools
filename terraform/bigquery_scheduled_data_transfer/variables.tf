variable "destination_dataset_id" {
  type        = string
  default     = null
  description = "The destination dataset to load the data into (if any)."
}

variable "destination_table_name_template" {
  type        = string
  default     = null
  description = "The destination table to load the data into (if any)."
}

variable "enable_auto_scheduling" {
  type        = bool
  default     = false
  description = "Whether this data transfer should be scheduled as soon as its deployed (production), or only triggered by hand (development)."
}

variable "interval" {
  type        = string
  description = "the interval at which this query should be executed, also affects `interval` variable available inside the query"
}

variable "labels" {
  default     = {}
  description = "Labels that should be passed to the Google Cloud resource"
  type        = map(string)
}

variable "location" {
  type        = string
  description = "Google Cloud location used to execute the data transfer. To reduce costs it is recommended to keep this the same as the tables where data is transferred from/to."
}


variable "name" {
  type        = string
  description = "A unique (display) name describing this data transfer"
}

variable "query_template" {
  type        = string
  description = "The path to query to execute. Your SQL can make use of the `interval` variable to slice data to the proper time period."
}

variable "query_variables" {
  type        = map(string)
  default     = {}
  description = "Optional variables to pass to your query template."
}

variable "service_account_email" {
  type        = string
  default     = null
  description = "Service account emailaddress used for executing the scheduled data transfer."
}

variable "write_disposition" {
  type        = string
  default     = null
  description = <<EOF
Specifies the action that occurs if the destination table already exists. The following values are supported:

    WRITE_TRUNCATE: If the table already exists, BigQuery overwrites the table data and uses the schema from the query result.
    WRITE_APPEND: If the table already exists, BigQuery appends the data to the table.
    WRITE_EMPTY: If the table already exists and contains data, a 'duplicate' error is returned in the job result.

The default value is WRITE_EMPTY. Each action is atomic and only occurs if BigQuery is able to complete the job successfully. Creation, truncation and append actions occur as one atomic update upon job completion."
EOF
}
