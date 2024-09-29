module "aws_vpc" {
  source = "./vpc"

  env    = var.env
  region = var.region
  name   = "docto-technical-case-vpc"
}

module "aws_rds" {
  source = "./rds"

  env    = var.env
  region = var.region
  name   = "docto-technical-case-db"

  vpc_id              = module.aws_vpc.id
  vpc_private_subnets = module.aws_vpc.private_subnets
  sg_ec2_id           = module.aws_ec2.sg_id
}

module "aws_ec2" {
  source = "./ec2"

  env    = var.env
  region = var.region
  name   = "docto-technical-case-ec2"

  vpc_private_subnets = module.aws_vpc.private_subnets
  vpc_public_subnets  = module.aws_vpc.public_subnets
  vpc_nat_gateways    = module.aws_vpc.nat_gateways
  vpc_id              = module.aws_vpc.id

  mysql_db       = module.aws_rds.db_name
  mysql_user     = module.aws_rds.db_user
  mysql_password = module.aws_rds.db_password
  mysql_host     = split(":", module.aws_rds.db_endpoint)[0]
  mysql_port     = split(":", module.aws_rds.db_endpoint)[1]
}

