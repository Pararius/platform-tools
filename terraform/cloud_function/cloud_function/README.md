<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_google"></a> [google](#provider\_google) | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_archive_prefixed"></a> [archive\_prefixed](#module\_archive\_prefixed) | ./../archive_file_prefixed | n/a |
| <a name="module_archive_selective"></a> [archive\_selective](#module\_archive\_selective) | ./../archive_file_selective | n/a |

## Resources

| Name | Type |
|------|------|
| [google_cloud_scheduler_job.scheduler_job](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloud_scheduler_job) | resource |
| [google_cloudfunctions_function.http_function](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudfunctions_function) | resource |
| [google_cloudfunctions_function.pubsub_function](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudfunctions_function) | resource |
| [google_storage_bucket_object.function_source_code](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket_object) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_function_entry_point"></a> [function\_entry\_point](#input\_function\_entry\_point) | The name of the function that is called in your source code when the Cloud Function is triggered. | `string` | `"handler"` | no |
| <a name="input_function_env_vars"></a> [function\_env\_vars](#input\_function\_env\_vars) | Environment variables that are passed to the Cloud Function and can be used to provide additional configuration. | `map(any)` | `{}` | no |
| <a name="input_function_max_instances"></a> [function\_max\_instances](#input\_function\_max\_instances) | The maximum number of Cloud Function instances that should be running at any time. | `number` | `1000` | no |
| <a name="input_function_memory"></a> [function\_memory](#input\_function\_memory) | The amount of memory (in megabytes) that the Cloud Function instance is allowed to consume. | `number` | `128` | no |
| <a name="input_function_min_instances"></a> [function\_min\_instances](#input\_function\_min\_instances) | The minimum number of Cloud Function instances that should be running at any time. | `number` | `0` | no |
| <a name="input_function_name"></a> [function\_name](#input\_function\_name) | A unique identity for this function, must be different than other functions you have in your project AND terraform workspaces (should include suffix!). | `string` | n/a | yes |
| <a name="input_function_retry_on_failure"></a> [function\_retry\_on\_failure](#input\_function\_retry\_on\_failure) | Indicates whether the function should be retried on failure. Only applies when you expect your code to fail now and then. | `bool` | `false` | no |
| <a name="input_function_runtime"></a> [function\_runtime](#input\_function\_runtime) | The runtime used to execute your code, see https://cloud.google.com/functions/docs/runtime-support for more options. | `string` | `"python310"` | no |
| <a name="input_function_service_account_email"></a> [function\_service\_account\_email](#input\_function\_service\_account\_email) | The email address of the service account used to run the Cloud Function instance. You should male sure it has all the roles necessary to run your code. | `string` | n/a | yes |
| <a name="input_function_timeout"></a> [function\_timeout](#input\_function\_timeout) | The maximum time in seconds to allow for this function to run. Can not be more than 540. | `number` | `60` | no |
| <a name="input_function_type"></a> [function\_type](#input\_function\_type) | The type of Cloud Function used. Controls how the function is triggered. Can be either 'http' or 'pubsub' | `string` | `"http"` | no |
| <a name="input_function_vpc_connector"></a> [function\_vpc\_connector](#input\_function\_vpc\_connector) | When provided, this allows the function to connect to the outside world through a specific VPC. Useful for connecting with systems that have an IP whitelist. | `string` | `null` | no |
| <a name="input_function_vpc_connector_egress_settings"></a> [function\_vpc\_connector\_egress\_settings](#input\_function\_vpc\_connector\_egress\_settings) | Restricts the kind of traffic allowed to pass through the VPC connector. Allowed values are ALL\_TRAFFIC and PRIVATE\_RANGES\_ONLY. Defaults to PRIVATE\_RANGES\_ONLY. If unset, this field preserves the previously set value. | `string` | `null` | no |
| <a name="input_google_cloud_project_id"></a> [google\_cloud\_project\_id](#input\_google\_cloud\_project\_id) | The ID of the Google Cloud Project used to deploy this function. | `string` | n/a | yes |
| <a name="input_google_cloud_region"></a> [google\_cloud\_region](#input\_google\_cloud\_region) | The region used to deploy this function on Google Cloud. | `string` | n/a | yes |
| <a name="input_pubsub_topic_id"></a> [pubsub\_topic\_id](#input\_pubsub\_topic\_id) | The ID of the pubsub topic that this function should be triggered by (if any). Only works in conjunction with `type=pubsub`. | `string` | `null` | no |
| <a name="input_scheduler_service_account_email"></a> [scheduler\_service\_account\_email](#input\_scheduler\_service\_account\_email) | The email address of the service account used to schedule the Cloud Function instance (if configured to do so). You should make sure it has at least the `roles/cloudfunctions.invoker` role for it to work. | `string` | `null` | no |
| <a name="input_schedulers"></a> [schedulers](#input\_schedulers) | Specifies one or more intervals at which your Cloud Function should be triggered, and the request it should receive. | <pre>list(object({<br>    attempt_deadline = optional(string)<br>    name             = string<br>    schedule         = string<br>    request_body     = optional(string)<br>    request_method   = optional(string)<br>    retry_count      = optional(number)<br>  }))</pre> | `[]` | no |
| <a name="input_source_code_bucket_name"></a> [source\_code\_bucket\_name](#input\_source\_code\_bucket\_name) | The name of the bucket where source code for this function is stored. | `string` | n/a | yes |
| <a name="input_source_files"></a> [source\_files](#input\_source\_files) | Points to specific files that make up your function. It can only point to a single `main.py` but more files can be added to extend functionality. Conflicts with `source_prefix`. | `list(string)` | `[]` | no |
| <a name="input_source_prefix"></a> [source\_prefix](#input\_source\_prefix) | Points to the directory containing your function code. It should have at least a `main.py` file and an optional `requirements.txt` to install dependencies. Conflicts with `source_files`. | `string` | `null` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_https_trigger_url"></a> [https\_trigger\_url](#output\_https\_trigger\_url) | n/a |
| <a name="output_name"></a> [name](#output\_name) | n/a |
<!-- END_TF_DOCS -->