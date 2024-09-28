resource "aws_s3_bucket" "ec2" {
  bucket = var.name

  tags = {
    Name        = var.name
    Environment = var.env
    Terraform   = "true"
  }
}

resource "aws_s3_bucket_ownership_controls" "ec2" {
  bucket = aws_s3_bucket.ec2.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "ec2" {
  depends_on = [aws_s3_bucket_ownership_controls.ec2]

  bucket = aws_s3_bucket.ec2.id
  acl    = "private"
}

resource "aws_s3_object" "docker_compose" {
  bucket = aws_s3_bucket.ec2.id
  key    = "docker-compose.yaml"
  source = "ec2/files/docker-compose.yaml"

  tags = {
    Name        = "docker-compose.yamls"
    Environment = var.env
    Terraform   = "true"
  }
}
