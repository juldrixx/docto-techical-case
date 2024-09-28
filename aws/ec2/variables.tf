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
  description = "Private subnets the VPC"
}

variable "vpc_public_subnets" {
  type        = list(string)
  description = "Public subnets the VPC"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type"
  default     = "t2.micro"
}

variable "min_size" {
  type = number
  description = "Minimum number of EC2 instance"
  default = 2
}

variable "max_size" {
  type = number
  description = "Maximum number of EC2 instance"
  default = 5
}
