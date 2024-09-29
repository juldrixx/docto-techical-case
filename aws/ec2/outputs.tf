output "sg_id" {
  description = "Security Group Id for the EC2 instances"
  value       = aws_security_group.ec2.id
}

output "dns_name" {
  description = "DNS Name for the EC2 instances"
  value       = aws_lb.ec2.dns_name
}
