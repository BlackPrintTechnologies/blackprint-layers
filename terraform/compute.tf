# Get the latest Ubuntu 20.04 AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# EC2 Instance Role
resource "aws_iam_role" "ec2_role" {
  name = "${var.app_name}-ec2-role"

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
}

# EC2 Instance Profile
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.app_name}-ec2-profile"
  role = aws_iam_role.ec2_role.name
}

# Basic security group
resource "aws_security_group" "app" {
  name        = "${var.app_name}-sg"
  description = "Security group for ${var.app_name}"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.app_name}-sg"
  }
}

# EC2 Instance
resource "aws_instance" "app" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.medium"
  #to set storage to 30gb
  root_block_device {
    volume_size = 30  # set this to 30 GB
    volume_type = "gp2"
  }

  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name
  vpc_security_group_ids      = [aws_security_group.app.id]

  user_data = <<-EOF
              #!/bin/bash
              apt update -y
              apt install -y python3 python3-pip git
              pip3 install --upgrade pip
              cd /home/ubuntu
              git clone https://github.com/BlackPrintTechnologies/blackprint-layers
              cd blackprint-layers/layers_backend
              pip3 install -r requirements.txt
              # Start the FastAPI app (will fail until app.json is added manually)
              nohup uvicorn main:app --host 0.0.0.0 --port 80 &
              EOF

  key_name = "my-key"

  tags = {
    Name = "${var.app_name}-instance"
  }
}
