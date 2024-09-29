resource "aws_security_group" "ec2" {
  name = "${var.name}-sg"

  description = "Security group for EC2 instance ${var.name}"
  vpc_id      = var.vpc_id

  ingress {
    description = "Allow all traffic through SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description     = "Allow ALB traffic through HTTP"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  ingress {
    description     = "Allow ALB traffic through for API"
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.name}-sg"
    Environment = var.env
    Terraform   = "true"
  }
}

resource "aws_launch_template" "ec2" {
  image_id      = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  vpc_security_group_ids = [aws_security_group.ec2.id]
  update_default_version = true

  metadata_options {
    http_tokens = "required"
  }

  iam_instance_profile {
    arn = aws_iam_instance_profile.ec2.arn
  }

  monitoring {
    enabled = true
  }

  user_data = base64encode(<<-EOF
              #!/bin/bash
              # Install Docker
              sudo apt-get update
              sudo apt-get install -y docker.io docker-compose awscli
              sudo usermod -aG docker $USER
              newgrp docker

              # Create a directory for the docker-compose file
              mkdir -p /home/ubuntu/app

              # Copy the docker-compose.yml from the S3 bucket
              aws s3 cp s3://${aws_s3_bucket.ec2.bucket}/${aws_s3_object.docker_compose.key} /home/ubuntu/app/docker-compose.yaml

              # Change to the app directory
              cd /home/ubuntu/app

              # Run Docker Compose
              docker-compose up -d
              EOF
  )
}

resource "aws_autoscaling_group" "ec2" {
  max_size            = var.max_size
  min_size            = var.min_size
  vpc_zone_identifier = var.vpc_private_subnets

  launch_template {
    id      = aws_launch_template.ec2.id
    version = aws_launch_template.ec2.latest_version
  }

  health_check_type         = "EC2"
  health_check_grace_period = 300

  tag {
    key                 = "Name"
    value               = var.name
    propagate_at_launch = true
  }
  tag {
    key                 = "Environment"
    value               = var.env
    propagate_at_launch = true
  }
  tag {
    key                 = "Terraform"
    value               = "true"
    propagate_at_launch = true
  }

  depends_on = [var.vpc_nat_gateways, aws_s3_object.docker_compose]
}
