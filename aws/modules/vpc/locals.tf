locals {
  azs             = slice(data.aws_availability_zones.available.names, 0, 3)
  public_subnets  = [for k, v in local.azs : cidrsubnet(var.cidr_block, 4, k)]
  private_subnets = [for k, v in local.azs : cidrsubnet(var.cidr_block, 8, k + 64)]
}
