terraform {
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 5.0"
        }
    }

    required_version = "= 1.9.6"

    backend "s3" {
        key    = "docto-techincal-case"
        region = var.region
    }
}