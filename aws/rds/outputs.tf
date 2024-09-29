output "db_name" {
  description = "RDS db name"
  value       = aws_db_instance.rds.db_name
}

output "db_user" {
  description = "RDS db user"
  value       = aws_db_instance.rds.username
}

output "db_password" {
  description = "RDS db password"
  value       = aws_db_instance.rds.password
  sensitive   = true
}

output "db_endpoint" {
  description = "RDS db endpoint"
  value       = aws_db_instance.rds.endpoint
}
