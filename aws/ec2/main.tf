resource "aws_security_group" "ec2_sg" {
  name = "${var.name}-sg"

  description = "Security group for EC2 instance ${var.name}"
  vpc_id      = var.vpc_id

  # ingress {
  #   description = "Allow all traffic through HTTP"
  #   from_port   = 80
  #   to_port     = 80
  #   protocol    = "tcp"
  #   cidr_blocks = ["0.0.0.0/0"]
  # }

  # ingress {
  #   description = "Allow SSH traffic from my computer"
  #   from_port   = "22"
  #   to_port     = "22"
  #   protocol    = "tcp"
  #   cidr_blocks = ["2.15.169.232/32"]
  # }

  ingress {
    description     = "Allow ALB traffic through HTTP"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = var.env
    Terraform   = "true"
  }
}

# resource "aws_key_pair" "tutorial_kp" {
#   key_name   = "tutorail_kp"
#   public_key = file("ec2/files/tutorial_kp.pub")
# }

resource "aws_launch_template" "ec2_instance" {
  image_id      = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  update_default_version = true

  # key_name = aws_key_pair.tutorial_kp.key_name

  iam_instance_profile {
    arn = aws_iam_instance_profile.ec2_instance_profile.arn
  }

  monitoring {
    enabled = true
  }

  # network_interfaces {
  #   associate_public_ip_address = true
  #   security_groups             = [aws_security_group.ec2_sg.id]
  # }

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
              aws s3 cp s3://${aws_s3_bucket.ec2_bucket.bucket}/${aws_s3_object.docker_compose.key} /home/ubuntu/app/docker-compose.yaml

              # Change to the app directory
              cd /home/ubuntu/app

              # Run Docker Compose
              docker-compose up -d
              EOF
  )
}

resource "aws_autoscaling_group" "ec2_asg" {
  max_size            = var.max_size
  min_size            = var.min_size
  vpc_zone_identifier = var.vpc_public_subnets

  launch_template {
    id      = aws_launch_template.ec2_instance.id
    version = aws_launch_template.ec2_instance.latest_version
  }

  health_check_type         = "EC2"
  health_check_grace_period = 300

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
}

resource "aws_cloudwatch_log_group" "ec2_log_group" {
  name              = "/ec2/logs"
  retention_in_days = 7
}
