# AWS

## Requirements

### Access Management

#### Policies

In some case the default policies proposed by AWS aren't sufficient. So we need to create our own.
For example, when using KMS resources (Key Management Service), there isn't a policy that allows to create a key and at the same time to use it with an other resource like RDS.

Create a custom policy named `AWSKeyManagementServiceFullAccess` with the following configuration:

```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": "kms:*",
			"Resource": "*"
		}
	]
}
```

#### User

To perform action on AWS, with Terraform for example, you need to have the credentials of a User with the correct rights.

Create an AWS User through the AWS Console with the following policies attached to it:

- AmazonEC2FullAccess: Allow us to manage EC2 resources
- AmazonRDSFullAccess: Allow us to manage RDS resources
- AmazonS3FullAccess: Allow us to manage S3 resources
- IAMFullAccess: Allow us to manage IAM resources
- AWSKeyManagementServiceFullAccess: Allow us to manage KMS resources

Create an Access Key and retrieve its key and secret.
Set the 2 environment variables with it:

```sh
export AWS_ACCESS_KEY_ID=<HIDE>
export AWS_SECRET_ACCESS_KEY=<HIDE>
```

> You can put theses exports in your `~/.bashrc` or directely put the variables in `/etc/environment`.

#### Role

TODO

### S3 Bucket for Terraform state

When using Terraform, you prefer to store your Terraform state in the same infrastructure that your working on.
So when using Terraform on AWS, you will store your state in an S3 bucket for it.

Create an S3 bucket:

```sh
aws s3api create-bucket \
  --bucket tf-docto-technical-case \
  --region eu-west-3 \
  --create-bucket-configuration LocationConstraint=eu-west-3
```

> We set the region as `eu-west-3` that represents Paris, because it will reduce our network costs.

Delete S3 bucket for TF State:

```sh
aws s3api delete-bucket \
  --bucket tf-docto-technical-case \
  --region eu-west-3 
```

## Notes

### VPC

When creating a VPC, you will need to make it available in your region but also accross multiple zones of this region to prevent downtime in case of a zone failure.

Using the `aws_availability_zones` when can get the zones available in the selected region.

```tf
data "aws_availability_zones" "available" {
  filter {
    name   = "opt-in-status"
    values = ["opt-in-not-required"]
  }
}s
```

But we don't need our VPC to be present in all the zones of the region, most of the time 3 zones are sufficient.
That is why we are slicing the list to get only 3 zones.

```
locals {
  azs = slice(data.aws_availability_zones.available.names, 0, 3)
}
```

After that, using our defined CIDR `cidr = "10.0.0.0/16"`, that represent the VPC IP range, we are creating private and public subnets in these zones, making sure that the IPs addresses of these subnets do not overlap.

```tf
public_subnets = [for k, v in local.azs : cidrsubnet("10.0.0.0/16", 4, k)]
private_subnets = [for k, v in local.azs : cidrsubnet("10.0.0.0/16", 8, k + 64)]
```

> If we create several VPCs, for example one per environment, we can use the same CIDR only if we don't want to peer our VPCs to each other to enable communication between them.

And finally, we are creating a NAT gateway, to allow the resources in our VPC to communicate with external resources such as AWS or Internet ones (but not the other way around).