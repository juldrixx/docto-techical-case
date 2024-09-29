output "dns_name" {
  description = "DNS to access the website and fastapi"
  value       = module.aws_ec2.dns_name
}