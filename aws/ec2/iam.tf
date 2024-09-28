resource "aws_iam_role" "ec2" {
  name = "${var.name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.name}-role"
    Environment = var.env
    Terraform   = "true"
  }
}


resource "aws_iam_policy" "s3_access" {
  name        = "${var.name}-s3-bucket"
  description = "Policy to allow access to S3 bucket ${aws_s3_bucket.ec2.bucket}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
        ]
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.ec2.bucket}",
          "arn:aws:s3:::${aws_s3_bucket.ec2.bucket}/*"
        ]
      },
    ]
  })

  tags = {
    Name        = "${var.name}-s3-bucket"
    Environment = var.env
    Terraform   = "true"
  }
}

resource "aws_iam_role_policy_attachment" "s3" {
  role       = aws_iam_role.ec2.name
  policy_arn = aws_iam_policy.s3_access.arn
}

resource "aws_iam_instance_profile" "ec2" {
  name = "${var.name}-instance-profile"
  role = aws_iam_role.ec2.name

  tags = {
    Name        = "${var.name}-instance-profile"
    Environment = var.env
    Terraform   = "true"
  }
}
