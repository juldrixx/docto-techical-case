data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"]
}

data "template_file" "docker_compose" {
  template = file("ec2/files/docker-compose.yaml.tpl")
  vars = {
    fastapi_dns  = aws_lb.ec2.dns_name
    fastapi_path = var.fastapi_root_path
  }
}
