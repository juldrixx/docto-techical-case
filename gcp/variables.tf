variable "project_id" {
  type        = string
  description = "The project ID to host resources."
}

variable "region" {
  type        = string
  description = "Main region"
  default     = "europe-west1"
}
