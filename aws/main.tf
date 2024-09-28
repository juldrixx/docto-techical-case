module "aws_vpc" {
  source = "./vpc"

  env    = var.env
  region = var.region
}

module "aws_ec2" {
  source = "./ec2"

  env                 = var.env
  region              = var.region
  name                = "docto-technical-case-ec2"
  vpc_private_subnets = module.aws_vpc.private_subnets
  vpc_public_subnets  = module.aws_vpc.public_subnets
  vpc_id              = module.aws_vpc.id
}

module "aws_rds" {
  source = "./rds"

  env                 = var.env
  region              = var.region
  name                = "docto-technical-case-db"
  vpc_id              = module.aws_vpc.id
  vpc_private_subnets = module.aws_vpc.private_subnets
  sg_ec2_id           = module.aws_ec2.sg_id
}
