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
| <a name="module_custom_loader"></a> [custom\_loader](#module\_custom\_loader) | ./../cloud_function | n/a |

## Resources

| Name | Type |
|------|------|
| [google_pubsub_subscription.custom_extractor](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_subscription) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_custom_environment_variables"></a> [custom\_environment\_variables](#input\_custom\_environment\_variables) | Variables that you would like to have available to your custom loader | `map(string)` | `{}` | no |
| <a name="input_custom_source_code"></a> [custom\_source\_code](#input\_custom\_source\_code) | Path to the directory that will be used as source code for the loading stage. | `string` | n/a | yes |
| <a name="input_google_cloud_project_id"></a> [google\_cloud\_project\_id](#input\_google\_cloud\_project\_id) | The ID of the Google Cloud Project used to deploy this function. | `string` | n/a | yes |
| <a name="input_google_cloud_region"></a> [google\_cloud\_region](#input\_google\_cloud\_region) | The region used to deploy this function on Google Cloud. | `string` | n/a | yes |
| <a name="input_name"></a> [name](#input\_name) | Name used to identify this collection of resources, automatically gets suffixed with `suffix` variable. | `string` | n/a | yes |
| <a name="input_pubsub_topic_id"></a> [pubsub\_topic\_id](#input\_pubsub\_topic\_id) | The full PubSub topic ID that this loader should subscribe to (should start with projects/[project-id]/...). | `string` | n/a | yes |
| <a name="input_service_account_email"></a> [service\_account\_email](#input\_service\_account\_email) | The Service Account used to run (and optionally, schedule) the cloud functions needed for each step. | `string` | n/a | yes |
| <a name="input_source_code_bucket_name"></a> [source\_code\_bucket\_name](#input\_source\_code\_bucket\_name) | The bucket used to store the source code needed to run a step. | `string` | n/a | yes |
| <a name="input_suffix"></a> [suffix](#input\_suffix) | The suffix added to all resource names in order to differentiate environments (e.g. a feature branch or production) on Google Cloud. | `string` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->