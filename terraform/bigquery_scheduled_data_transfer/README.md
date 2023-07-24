<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_google"></a> [google](#provider\_google) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [google_bigquery_data_transfer_config.default](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_data_transfer_config) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_destination_table_name_template"></a> [destination\_table\_name\_template](#input\_destination\_table\_name\_template) | The destination table to load the data into (if any). | `string` | `null` | no |
| <a name="input_enable_auto_scheduling"></a> [enable\_auto\_scheduling](#input\_enable\_auto\_scheduling) | Whether this data transfer should be scheduled as soon as its deployed (production), or only triggered by hand (development). | `bool` | `false` | no |
| <a name="input_interval"></a> [interval](#input\_interval) | the interval at which this query should be executed, also affects `interval` variable available inside the query | `string` | n/a | yes |
| <a name="input_location"></a> [location](#input\_location) | Google Cloud location used to execute the data transfer. To reduce costs it is recommended to keep this the same as the tables where data is transferred from/to. | `string` | n/a | yes |
| <a name="input_name"></a> [name](#input\_name) | A unique (display) name describing this data transfer | `string` | n/a | yes |
| <a name="input_query_template"></a> [query\_template](#input\_query\_template) | The path to query to execute. Your SQL can make use of the `interval` variable to slice data to the proper time period. | `string` | n/a | yes |
| <a name="input_query_variables"></a> [query\_variables](#input\_query\_variables) | Optional variables to pass to your query template. | `map(string)` | `{}` | no |
| <a name="input_write_disposition"></a> [write\_disposition](#input\_write\_disposition) | Specifies the action that occurs if the destination table already exists. The following values are supported:<br><br>    WRITE\_TRUNCATE: If the table already exists, BigQuery overwrites the table data and uses the schema from the query result.<br>    WRITE\_APPEND: If the table already exists, BigQuery appends the data to the table.<br>    WRITE\_EMPTY: If the table already exists and contains data, a 'duplicate' error is returned in the job result.<br><br>The default value is WRITE\_EMPTY. Each action is atomic and only occurs if BigQuery is able to complete the job successfully. Creation, truncation and append actions occur as one atomic update upon job completion." | `string` | `null` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->