# Create VPC
resource "aws_vpc" "vpc" {
  cidr_block = var.cidr_block

  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = var.name
    Environment = var.env
    Terraform   = "true"
  }
}

# Create CloudWatch Log Group
resource "aws_cloudwatch_log_group" "vpc" {
  name              = "vpc-flow-logs"
  retention_in_days = 1
  kms_key_id        = var.kms_key_arn
}

# Create Flow Log
resource "aws_flow_log" "vpc" {
  vpc_id          = aws_vpc.vpc.id
  iam_role_arn    = aws_iam_role.vpc.arn
  log_destination = aws_cloudwatch_log_group.vpc.arn
  traffic_type    = "ALL"
}

# Create Public Subnets
resource "aws_subnet" "publics" {
  count = length(local.public_subnets)

  vpc_id            = aws_vpc.vpc.id
  cidr_block        = element(local.public_subnets, count.index)
  availability_zone = element(local.azs, count.index)

  tags = {
    Name        = "${var.name}-public-subnet-${count.index}"
    Environment = var.env
    Terraform   = "true"
  }
}

# Create Private Subnets
resource "aws_subnet" "privates" {
  count = length(local.private_subnets)

  vpc_id            = aws_vpc.vpc.id
  cidr_block        = element(local.private_subnets, count.index)
  availability_zone = element(local.azs, count.index)

  tags = {
    Name        = "${var.name}-private-subnet-${count.index}"
    Environment = var.env
    Terraform   = "true"
  }
}

# Create Internet GateWay
resource "aws_internet_gateway" "public" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name        = "${var.name}-public-igw"
    Environment = var.env
    Terraform   = "true"
  }
}

# Create Public Route Table
resource "aws_route_table" "publics" {
  count = length(local.public_subnets)

  vpc_id = aws_vpc.vpc.id

  tags = {
    Name        = "${var.name}-public-route-table-${count.index}"
    Environment = var.env
    Terraform   = "true"
  }
}

# Create Public Route Association
resource "aws_route_table_association" "publics" {
  count = length(local.public_subnets)

  route_table_id = element(aws_route_table.publics[*].id, count.index)
  subnet_id      = element(aws_subnet.publics[*].id, count.index)
}

# Add Internet Gateway to Public Route Table
resource "aws_route" "internet_gateway" {
  count = length(local.public_subnets)

  route_table_id         = element(aws_route_table.publics[*].id, count.index)
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.public.id
}

# Create Private Route Table
resource "aws_route_table" "privates" {
  count = length(local.private_subnets)

  vpc_id = aws_vpc.vpc.id

  tags = {
    Name        = "${var.name}-private-route-table-${count.index}"
    Environment = var.env
    Terraform   = "true"
  }
}

# Create Private Route Association
resource "aws_route_table_association" "privates" {
  count = length(local.private_subnets)

  route_table_id = element(aws_route_table.privates[*].id, count.index)
  subnet_id      = element(aws_subnet.privates[*].id, count.index)
}

# Create Elastic IP
resource "aws_eip" "nat_gateways" {
  count  = length(aws_subnet.publics)
  domain = "vpc"

  tags = {
    Name        = "${var.name}-public-eip-${count.index}"
    Environment = var.env
    Terraform   = "true"
  }
}

# Create Public NatGateway
resource "aws_nat_gateway" "publics" {
  count = length(aws_subnet.publics)

  subnet_id     = element(aws_subnet.publics[*].id, count.index)
  allocation_id = element(aws_eip.nat_gateways[*].id, count.index)

  tags = {
    Name        = "${var.name}-public-net-gateway-${count.index}"
    Environment = var.env
    Terraform   = "true"
  }

  depends_on = [aws_internet_gateway.public]
}

# Add NatGateway to Private Route Table
resource "aws_route" "nat_gateway" {
  count = length(aws_subnet.publics)

  route_table_id         = element(aws_route_table.privates[*].id, count.index)
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = element(aws_nat_gateway.publics[*].id, count.index)
}
