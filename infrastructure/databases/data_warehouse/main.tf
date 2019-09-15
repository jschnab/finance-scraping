terraform {
  required_version = ">= 0.12, < 0.13"

  # we only provide the key, bucket and region and provided
  # through the backend configuration file
  backend "s3" {
    key = "dev/databases/rds/terraform.tfstate"
  }
}

provider "aws" {
  version = "~> 2.0"
  region = "us-east-1"
  profile = var.aws_profile
}

resource "aws_db_instance" "rds_db" {
  # only alphanumeric characters and hyphens are allowed for identifier_prefix
  identifier_prefix = replace(var.db_name, "/[^a-zA-Z0-9]/", "-")
  engine = var.db_engine
  allocated_storage = var.db_storage
  instance_class = var.db_instance_class
  name = var.db_name
  username = var.db_username
  password = var.db_password
  db_subnet_group_name = aws_db_subnet_group.private_subnets_group.id
  skip_final_snapshot = true
}

resource "aws_db_subnet_group" "private_subnets_group" {
  name = "finance-db-private-subnets"
  subnet_ids = [
    data.terraform_remote_state.network.outputs.private_subnet_1_id,
    data.terraform_remote_state.network.outputs.private_subnet_2_id
  ]
  description = "Group of private subnets to place the RDS instance in"
  tags = { Name = "finance-db-private-subnets-group" }
}

data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = var.state_bucket
		key = "global/network/terraform.tfstate"
		region = "us-east-1"
  }
}
