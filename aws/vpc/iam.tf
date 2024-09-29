resource "aws_iam_role" "vpc" {
  name = "${vpc}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Principal = {
          Service = "vpc-flow-logs.amazonaws.com"
        }
        Effect = "Allow"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "flow_logs_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWS_VPC_FlowLogs"
  role       = aws_iam_role.vpc.name
}
