#tfsec:ignore:aws-s3-enable-bucket-logging
#tfsec:ignore:aws-s3-enable-versioning
resource "aws_s3_bucket" "ec2" {
  bucket = var.name

  tags = {
    Name        = var.name
    Environment = var.env
    Terraform   = "true"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "ec2" {
  bucket = aws_s3_bucket.ec2.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = var.kms_key_arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_ownership_controls" "ec2" {
  bucket = aws_s3_bucket.ec2.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "ec2" {
  bucket = aws_s3_bucket.ec2.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_acl" "ec2" {
  depends_on = [aws_s3_bucket_ownership_controls.ec2]

  bucket = aws_s3_bucket.ec2.id
  acl    = "private"
}

resource "aws_s3_object" "docker_compose" {
  bucket  = aws_s3_bucket.ec2.id
  key     = "docker-compose.yaml"
  content = data.template_file.docker_compose.rendered

  tags = {
    Name        = "docker-compose.yaml"
    Environment = var.env
    Terraform   = "true"
  }
}

#tfsec:ignore:aws-s3-enable-bucket-logging
#tfsec:ignore:aws-s3-enable-versioning
resource "aws_s3_bucket" "data" {
  bucket        = "${var.name}-data"
  force_destroy = true

  tags = {
    Name        = "${var.name}-data"
    Environment = var.env
    Terraform   = "true"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = var.kms_key_arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_ownership_controls" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_acl" "data" {
  depends_on = [aws_s3_bucket_ownership_controls.data]

  bucket = aws_s3_bucket.data.id
  acl    = "private"
}
