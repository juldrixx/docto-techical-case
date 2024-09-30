#tfsec:ignore:aws-ec2-no-public-ingress-sgr
#tfsec:ignore:aws-ec2-no-public-egress-sgr
resource "aws_security_group" "alb" {
  name = "${var.name}-alb-sg"

  description = "Security group for ALB instance ${var.name}"
  vpc_id      = var.vpc_id

  ingress {
    description = "Allow all traffic through HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow all traffic through HTTPs"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.name}-alb-sg"
    Environment = var.env
    Terraform   = "true"
  }
}

#tfsec:ignore:aws-elb-alb-not-public
resource "aws_lb" "ec2" {
  name                       = "${var.name}-alb"
  load_balancer_type         = "application"
  internal                   = false
  security_groups            = [aws_security_group.alb.id]
  subnets                    = var.vpc_public_subnets
  drop_invalid_header_fields = true

  tags = {
    Name        = "${var.name}-alb"
    Environment = var.env
    Terraform   = "true"
  }
}

resource "aws_alb_target_group" "website" {
  name     = "${var.name}-website"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path                = "/"
    port                = "traffic-port"
    healthy_threshold   = 5
    unhealthy_threshold = 2
    timeout             = 2
    interval            = 60
    matcher             = "200"
  }

  tags = {
    Name        = "${var.name}-website"
    Environment = var.env
    Terraform   = "true"
  }
}

resource "aws_alb_target_group" "fastapi" {
  name     = "${var.name}-fastapi"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path                = "/"
    port                = "traffic-port"
    healthy_threshold   = 5
    unhealthy_threshold = 2
    timeout             = 2
    interval            = 60
    matcher             = "200"
  }

  tags = {
    Name        = "${var.name}-fastapi"
    Environment = var.env
    Terraform   = "true"
  }
}

resource "aws_autoscaling_attachment" "fastapi" {
  autoscaling_group_name = aws_autoscaling_group.ec2.id
  lb_target_group_arn    = aws_alb_target_group.fastapi.arn
}

resource "aws_autoscaling_attachment" "website" {
  autoscaling_group_name = aws_autoscaling_group.ec2.id
  lb_target_group_arn    = aws_alb_target_group.website.arn
}

#tfsec:ignore:aws-elb-http-not-used
resource "aws_alb_listener" "ec2" {
  load_balancer_arn = aws_lb.ec2.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "Resource not found"
      status_code  = "404"
    }
  }

  tags = {
    Name        = var.name
    Environment = var.env
    Terraform   = "true"
  }
}

resource "aws_lb_listener_rule" "website" {
  listener_arn = aws_alb_listener.ec2.arn
  priority     = 200

  action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.website.arn
  }

  condition {
    path_pattern {
      values = ["/*"]
    }
  }
}

resource "aws_lb_listener_rule" "fastapi" {
  listener_arn = aws_alb_listener.ec2.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.fastapi.arn
  }


  condition {
    path_pattern {
      values = ["${var.fastapi_root_path}*"]
    }
  }
}
