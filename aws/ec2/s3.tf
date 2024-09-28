resource "aws_s3_bucket" "ec2_bucket" {
  bucket = var.name
}

resource "aws_s3_object" "docker_compose" {
  bucket = aws_s3_bucket.ec2_bucket.bucket
  key    = "docker-compose.yaml"
  source = "ec2/files/docker-compose.yaml"
}
