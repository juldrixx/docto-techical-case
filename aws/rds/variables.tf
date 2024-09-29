variable "env" {
  type        = string
  description = "Formatted env. Ex `dev` or `prd`"
}

variable "region" {
  type        = string
  description = "AWS region for the Provider"
}

variable "name" {
  type        = string
  description = "Name of the database"
}

variable "instance_class" {
  type        = string
  description = "RDS instance class"
  default     = "db.t3.micro"
}

variable "engine" {
  type        = string
  description = "Database engine"
  default     = "mysql"
}

variable "engine_version" {
  type        = string
  description = "Database engine version"
  default     = "8.0"
}

variable "vpc_id" {
  type        = string
  description = "Id of the VPC"
}

variable "vpc_private_subnets" {
  type        = list(string)
  description = "Private subnets the VPC"
}

variable "sg_ec2_id" {
  type        = string
  description = "Security Group Id for the EC2 instance"
}

variable "kms_key_arn" {
  type        = string
  description = "KMS Key ARN"
}
