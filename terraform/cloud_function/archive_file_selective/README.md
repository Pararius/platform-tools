<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [archive_file.source](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_files"></a> [files](#input\_files) | A list of (relative or absolute) paths to the files you want to include in the archive. | `list(string)` | n/a | yes |
| <a name="input_name"></a> [name](#input\_name) | A unique identity for this archived file | `string` | n/a | yes |
| <a name="input_type"></a> [type](#input\_type) | The type of archive file to produce | `string` | `"zip"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_output_md5"></a> [output\_md5](#output\_output\_md5) | n/a |
| <a name="output_output_path"></a> [output\_path](#output\_output\_path) | n/a |
<!-- END_TF_DOCS -->