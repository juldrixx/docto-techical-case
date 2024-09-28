locals {
  azs             = slice(data.aws_availability_zones.available.names, 0, 3)
  public_subnets  = [for k, v in local.azs : cidrsubnet("10.0.0.0/16", 4, k)]
  private_subnets = [for k, v in local.azs : cidrsubnet("10.0.0.0/16", 8, k + 64)]
}
