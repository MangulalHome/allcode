terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}

# Data source to get the latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "state"
    values = ["available"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# EC2 Instance Resource
resource "aws_instance" "asecurityguru" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t2.micro"
  
  tags = {
    Name = "ASecurityGuru"
  }
}

# Output the instance details
output "instance_id" {
  value       = aws_instance.asecurityguru.id
  description = "The ID of the EC2 instance"
}

output "instance_public_ip" {
  value       = aws_instance.asecurityguru.public_ip
  description = "The public IP address of the EC2 instance"
}

output "instance_ami" {
  value       = aws_instance.asecurityguru.ami
  description = "The AMI ID used for the instance"
}
