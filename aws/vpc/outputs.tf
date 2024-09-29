output "id" {
  description = "VPC Id"
  value       = aws_vpc.vpc.id
}

output "private_subnets" {
  description = "VPC Private Subnet Ids"
  value       = aws_subnet.privates[*].id
}

output "public_subnets" {
  description = "VPC Public Subnet Ids"
  value       = aws_subnet.publics[*].id
}

output "nat_gateways" {
  description = "VPC Nat Gateway Ids"
  value       = aws_nat_gateway.publics[*].id
}
