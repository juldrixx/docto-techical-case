<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | = 1.9.6 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.69.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_aws_ec2"></a> [aws\_ec2](#module\_aws\_ec2) | ./modules/ec2 | n/a |
| <a name="module_aws_rds"></a> [aws\_rds](#module\_aws\_rds) | ./modules/rds | n/a |
| <a name="module_aws_vpc"></a> [aws\_vpc](#module\_aws\_vpc) | ./modules/vpc | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_kms_key.kms_key](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/kms_key) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_cidr_block"></a> [cidr\_block](#input\_cidr\_block) | CIDR block | `string` | `"10.0.0.0/16"` | no |
| <a name="input_env"></a> [env](#input\_env) | Formatted env. Ex `dev` or `prd` | `string` | n/a | yes |
| <a name="input_region"></a> [region](#input\_region) | AWS region for the Provider | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_dns_name"></a> [dns\_name](#output\_dns\_name) | DNS to access the website and fastapi |
<!-- END_TF_DOCS -->