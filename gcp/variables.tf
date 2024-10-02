variable "env" {
  type        = string
  description = "Formatted env. Ex `dev` or `prd`"
}

variable "project_id" {
  type        = string
  description = "The project ID to host resources."
}

variable "region" {
  type        = string
  description = "Main region"
  default     = "europe-west1"
}