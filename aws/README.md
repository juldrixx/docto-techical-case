# AWS

## Requirements

### Access Management

#### Policies

In some case the default policies proposed by AWS aren't sufficient. So we need to create our own.
For example, when using KMS resources (Key Management Service), there isn't a policy that allows to create a key and at the same time to use it with an other resource like RDS.

Create a custom policy named `AWSKeyManagementServiceFullAccess` with the following configuration:

```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": "kms:*",
			"Resource": "*"
		}
	]
}
```

#### User

To perform action on AWS, with Terraform for example, you need to have the credentials of a User with the correct rights.

Create an AWS User through the AWS Console with the following policies attached to it:

- AmazonEC2FullAccess: Allow us to manage EC2 resources
- AmazonRDSFullAccess: Allow us to manage RDS resources
- AmazonS3FullAccess: Allow us to manage S3 resources
- IAMFullAccess: Allow us to manage IAM resources
- AWSKeyManagementServiceFullAccess: Allow us to manage KMS resources

Create an Access Key and retrieve its key and secret.
Set the 2 environment variables with it:

```sh
export AWS_ACCESS_KEY_ID=<HIDE>
export AWS_SECRET_ACCESS_KEY=<HIDE>
```

> You can put theses exports in your `~/.bashrc` or directely put the variables in `/etc/environment`.

#### GitHub Actions

In GitHub Actions, we will run the different Terraform commands. But for doing that, the GitHub Actions must have access to AWS. We could do it the same way we did locally by using a user and set the different environment variables. But using the AWS credentials like that poses security risk, the credentials are generally long-lived and with a lot of permissions. So we don't want to have credentials and use a method that allows only our GitHub repository to have the rights.

The way to do it is by setting up the OpenID Connect in AWS.
Within AWS, we will have to create an Identity Provider for GitHub and a Rrole for Web Identity with the created Identity Provider attached to it.

##### Create GitHub Identity Provider

Navigate to `IAM > Identity providers` and create new one. Select `OpenID Connect` with the following configuration:
- Provider URL: `https://token.actions.githubusercontent.com`
- Audience: `sts.amazonaws.com`

##### Create AWS Role

Navigate to `IAM > Roles` and create new one. Select `Web Identity` with the following configuration:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::920373018420:oidc-provider/token.actions.githubusercontent.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                },
                "StringLike": {
                    "token.actions.githubusercontent.com:sub": "repo:juldrixx/docto-technical-case:ref:refs/heads/main"
                }
            }
        }
    ]
}
```

> Note,
> `"Federated": "arn:aws:iam::920373018420:oidc-provider/token.actions.githubusercontent.com"` references the created `Identity Provider` ARN.
> `"token.actions.githubusercontent.com:sub": "repo:juldrixx/docto-technical-case:ref:refs/heads/main"` will make sure that only our GitHub repository from its main branch can use this role.

#### Configure GitHub Action

Now, we can just configure our GitHub Action to use it.
You need to add these permissions:

```yaml
permissions:
  id-token: write # This is required for requesting the JWT
  contents: read  # This is required for actions/checkout
```

and the following action:

```yaml
- name: Configure aws credentials
  uses: aws-actions/configure-aws-credentials@v2
  with:
    role-to-assume: <ARN_ROLE>
    aws-region: eu-west-3
```

### S3 Bucket for Terraform state

When using Terraform, you prefer to store your Terraform state in the same infrastructure that your working on.
So when using Terraform on AWS, you will store your state in an S3 bucket for it.

Create an S3 bucket:

```sh
aws s3api create-bucket \
  --bucket tf-docto-technical-case \
  --region eu-west-3 \
  --create-bucket-configuration LocationConstraint=eu-west-3
```

> We set the region as `eu-west-3` that represents Paris, because it will reduce our network costs.

Delete S3 bucket for TF State:

```sh
aws s3api delete-bucket \
  --bucket tf-docto-technical-case \
  --region eu-west-3 
```

## Notes

### VPC

When creating a `VPC`, we need to make it available in your region but also accross multiple zones of this region to prevent downtime in case of a zone failure.

Using the `aws_availability_zones` when can get the zones available in the selected region.

```tf
data "aws_availability_zones" "available" {
  filter {
    name   = "opt-in-status"
    values = ["opt-in-not-required"]
  }
}s
```

But we don't need our `VPC` to be present in all the zones of the region, most of the time 3 zones are sufficient.
That is why we are slicing the list to get only 3 zones.

```
locals {
  azs = slice(data.aws_availability_zones.available.names, 0, 3)
}
```

After that, using our defined `CIDR` block `cidr_block = "10.0.0.0/16"`, that represent the `VPC` IP range, we are creating private and public subnets in these zones, making sure that the IPs addresses of these subnets do not overlap.

```tf
public_subnets = [for k, v in local.azs : cidrsubnet(var.cidr_block, 4, k)]
private_subnets = [for k, v in local.azs : cidrsubnet(var.cidr_block, 8, k + 64)]
```

> If we create several `VPCs`, for example one per environment, we can use the same `CIDR` only if we don't want to peer our VPCs to each other to enable communication between them.

And finally, we are creating `NAT Gateways` in each region, to allow the resources in our `VPC` to communicate with external resources such as AWS or Internet ones (but not the other way around).

### RDS

`RDS` allows us to create database in AWS. In our case, we chose to create a `MySQL` database. And placed it in our `Private Subnets` to prevent public access.
```tf
resource "aws_db_subnet_group" "rds_subnet_group" {
  subnet_ids = var.vpc_private_subnets
  ...
}

resource "aws_db_instance" "rds" {
  ...
  db_subnet_group_name    = aws_db_subnet_group.rds_subnet_group.name
  ...
}
```

But we don't want everything that is our `VPC` to be able to access it to prevent data leaks. To doing that we are creating a `Security Group` that will restrict access only on the port `3306` and from the `Security Group` where our `EC2 instances` are.
```tf
resource "aws_security_group" "rds_sg" {
  ...
  vpc_id      = var.vpc_id

  ingress {
    description     = "Allow ${upper(var.engine)} traffic from only the API Security Group"
    from_port       = "3306"
    to_port         = "3306"
    protocol        = "tcp"
    security_groups = [var.sg_ec2_id]
  }
}

resource "aws_db_instance" "rds" {
  ...
  vpc_security_group_ids  = [aws_security_group.rds_sg.id]
  ...
}
```

And to make our data safe, we will encrypt them using a `KMSKey`.
```tf
resource "aws_kms_key" "kms_key" {
  description = "Used to encrypt resources."
  ...
}

resource "aws_db_instance" "rds" {
  ...
  storage_encrypted       = true
  kms_key_id              = var.kms_key_arn
  ...
}
```

And by activating the automatic backup, we make sure that we can do `DR (Disaster Recovery)`. With a retention of 7 days (1 week), we are sure that in case of incident we can recover.
```tf
resource "aws_db_instance" "rds" {
  ...
  backup_retention_period = 7
  ...
}
```
> You can also trigger `Snapshot` and store them in a `S3 Bucket`. The backup occures only one time per day at fixed time, but you could take snapshots more often to mitigate the data loss.
> I desactivated the `Multi Availibity Zones` (`multi_az = false`) for cost reason (it free tier mode, it's not free) but in production use case, you want to activate it to increase your database availibity and robustness.

### EC2

An `EC2 instance` is in fact a `Virtual Machine` in my case an `Ubuntu` one. So can you to make it run what ever you want. In my case, I'm running Docker images on it. A docker image for my `FastApi` and an other one for my `Web site`.

But to make sure our infrastructure is robust and resilient, we need to make sure that in case of failure or increase of traffic, we still sufficient number of `EC2 instances` running.
That is why, we are creating our `EC2 Instances` using an `Auto Scaling Group`.
```tf
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
  ...
}
```
We are giving it a min and max number of instances, and AWS will make sure that our min is always respected and prevent us downtime. And the max will allow us to respond to an increase of traffic but liming our costs.

> Note that we specified that our `EC2 Instances` should be in our `Private Subnets` as we don't want them to be directly accessible publically.

Now, we need to indicate to our `Auto Scaling Group` what to run, for that we are using `Launch Template`.
```tf
resource "aws_launch_template" "ec2" {
  image_id      = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  ...
}
```
In it, we are specifying the image that we want to use. Here we are using the Ubuntu AMI from AWS.

Now that we have our `EC2 Instance`, we need to make something of it. We will run 2 docker images on it using `Docker Compose` but to do that we need the corresponding packages in the `EC2 Instance` and the `docker-compose.yaml` file.

For the `docker-compose.yaml`, we will have it locally with the Terraform and push it in an `S3 Bucket`.
```tf
data "template_file" "docker_compose" {
  template = file("${path.module}/files/docker-compose.yaml.tpl")
  vars = {
    fastapi_dns    = aws_lb.ec2.dns_name
    fastapi_path   = var.fastapi_root_path
    mysql_user     = var.mysql_user
    mysql_password = var.mysql_password
    mysql_host     = var.mysql_host
    mysql_port     = var.mysql_port
    mysql_db       = var.mysql_db
    s3_bucket      = aws_s3_bucket.data.bucket
  }
}

resource "aws_s3_object" "docker_compose" {
  bucket  = aws_s3_bucket.ec2.id
  key     = "docker-compose.yaml"
  content = data.template_file.docker_compose.rendered
  ...
}
```

And we create a `Role` that our `EC2 Instance` will assume that have read access on the bucket.
```tf
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

  ...
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
          "arn:aws:s3:::${aws_s3_bucket.ec2.bucket}/*",
        ]
      },
      ...
    ]
  })

  ...
}

resource "aws_iam_role_policy_attachment" "s3" {
  role       = aws_iam_role.ec2.name
  policy_arn = aws_iam_policy.s3_access.arn
}

resource "aws_iam_instance_profile" "ec2" {
  name = "${var.name}-instance-profile"
  role = aws_iam_role.ec2.name
  ...
}

resource "aws_launch_template" "ec2" {
  ...
  iam_instance_profile {
    arn = aws_iam_instance_profile.ec2.arn
  }
  ...
}
```

And now, we can configure our `EC2 Instance` to retrieve the file from the `S3 Bucket`, to install the mandatory packages and run the docker images.
```tf
resource "aws_launch_template" "ec2" {
  ...
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
```

Now, our `API` and `Web site` are running, but we need to communicate with `RDS` to store data in our database. So it's time, to configure the `Security Group` that has access to the `Security Group` of our `RDS`.
```tf
resource "aws_security_group" "ec2" {
  name = "${var.name}-sg"

  description = "Security group for EC2 instance ${var.name}"
  vpc_id      = var.vpc_id

  ingress {
    description = "Allow all traffic through SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.cidr_block]
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
  ...
}
```

As the `API` is exposed on the port `8000` and the `Web site` on `80`, we are allowing input request from the `Security Group` of our `Application Load Balancer` that will publically expose our `Web site` and `API`.

And we are also allowing output request for everywhere.

> Note that we are also allowing input connection in SSH for debugging purpose but only from with our VPC. So you need to use an `EC2 Instance Connect Endpoint` to access it.

We also create an `S3 Bucket` that will be used by the `API` to store data.
```tf
resource "aws_s3_bucket" "data" {
  bucket        = "${var.name}-data"
  force_destroy = true
  ...
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
```

> Note that the Bucket is publically not accessible and encrypted, it's the same for the bucket used for the `docker-compose.yaml` file.
> And we are authorizing to bucket to be destroyed with the data in it (`force_destroy = true`) only because its a technical case, otherwise by default it should be false and only if you are sure, you set it to true just before the deletion.

We changed the `hop rebound` for our `EC2 Instance` because otherwise, the docker container of the `API` couldn't access to S3.
```tf
resource "aws_launch_template" "ec2" {
  ...
  metadata_options {
    http_tokens                 = "required"
    http_put_response_hop_limit = 2
  }
  ...
}
```

Now that our application is running, we need to expose it to make it accessible to the user. For that, we use an `Application Load Balancer` place in our `Public Subnets`.
```tf
resource "aws_lb" "ec2" {
  name                       = "${var.name}-alb"
  load_balancer_type         = "application"
  internal                   = false
  security_groups            = [aws_security_group.alb.id]
  subnets                    = var.vpc_public_subnets
  drop_invalid_header_fields = true
  ...
}
```

The `Application Load Balancer` will listen all input request on the port `80`.
```tf
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
  ...
}

```

And we will tell him, to forward call on `/fastapî*` to our `API` exposed on the port `8000` of the `EC2 Instance` and all the call on `/*` to our `Web site` on port `80`.
```tf
variable "fastapi_root_path" {
  type        = string
  description = "Root path URL for the FastAPI"
  default     = "/fastapi"
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

  ...
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

  ...
}

resource "aws_autoscaling_attachment" "fastapi" {
  autoscaling_group_name = aws_autoscaling_group.ec2.id
  lb_target_group_arn    = aws_alb_target_group.fastapi.arn
}

resource "aws_autoscaling_attachment" "website" {
  autoscaling_group_name = aws_autoscaling_group.ec2.id
  lb_target_group_arn    = aws_alb_target_group.website.arn
}
```

And of course, we need to configure the `Security Group` for it. Allowing only input request in HTTP or HTTPs and all the output request. 
```tf
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
  ...
}
```