variable "env" {
  type        = string
  description = "Formatted env. Ex `dev` or `prd`"
}

variable "region" {
  type        = string
  description = "AWS region for the Provider"
}

variable "cidr_block" {
  type        = string
  description = "CIDR block"
  default     = "10.0.0.0/16"
}
