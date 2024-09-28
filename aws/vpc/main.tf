module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.13"

  name = "docto-technical-case-vpc"

  cidr = "10.0.0.0/16"
  azs  = local.azs

  private_subnets = [for k, v in local.azs : cidrsubnet("10.0.0.0/16", 4, k)]
  public_subnets  = [for k, v in local.azs : cidrsubnet("10.0.0.0/16", 8, k + 48)]

  enable_nat_gateway = true
  single_nat_gateway = true

  tags = {
    Environment = var.env
    Terraform   = "true"
  }
}
