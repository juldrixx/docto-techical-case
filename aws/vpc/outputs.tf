output "id" {
  value = aws_vpc.vpc.id
}

output "private_subnets" {
  value = aws_subnet.privates[*].id
}

output "public_subnets" {
  value = aws_subnet.publics[*].id
}

output "nat_gateways" {
  value = aws_nat_gateway.publics[*].id
}