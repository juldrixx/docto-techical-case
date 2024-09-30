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

variable "vpc_id" {
  type        = string
  description = "Id of the VPC"
}

variable "vpc_private_subnets" {
  type        = list(string)
  description = "Private subnets of the VPC"
}

variable "vpc_public_subnets" {
  type        = list(string)
  description = "Public subnets of the VPC"
}

variable "vpc_nat_gateways" {
  type        = list(string)
  description = "Nat gateways of the VPC"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type"
  default     = "t2.micro"
}

variable "min_size" {
  type        = number
  description = "Minimum number of EC2 instance"
  default     = 2
}

variable "max_size" {
  type        = number
  description = "Maximum number of EC2 instance"
  default     = 5
}

variable "fastapi_root_path" {
  type        = string
  description = "Root path URL for the FastAPI"
  default     = "/fastapi"
}

variable "mysql_user" {
  type        = string
  description = "MySQL user"
}

variable "mysql_password" {
  type        = string
  description = "MySQL password"
  sensitive   = true
}

variable "mysql_host" {
  type        = string
  description = "MySQL host"
}

variable "mysql_port" {
  type        = number
  description = "MySQL port"
}

variable "mysql_db" {
  type        = string
  description = "MySQL description"
}

variable "cidr_block" {
  type        = string
  description = "CIDR block"
}

variable "kms_key_arn" {
  type        = string
  description = "KMS Key ARN"
}
