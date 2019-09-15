terraform {
  required_version = ">= 0.12, < 0.13"
  backend "s3" {
    key = "dev/airflow-instance/terraform.tfstate"
  }
}

provider "aws" {
  version = "~> 2.0"
  region = "us-east-1"
  profile = var.aws_profile
}

module "airflow_instance" {
  source = "../modules/airflow-instance"

  instance_name = "airflow-instance"
  state_bucket = var.state_bucket
  db_remote_state_key = "dev/databases/rds/terraform.tfstate"
  iam_remote_state_key = "global/iam/terraform.tfstate"
  network_remote_state_key = "global/network/terraform.tfstate"
  instance_type = "t2.micro"
  custom_tags = {
    Owner = "Airflow"
    DeployedBy = "Terraform"
  }

  my_ip = var.my_ip
  ec2_ssh_key = var.ec2_ssh_key
  s3_bucket = var.data_bucket
  urls_s3_key = var.urls_s3_key
  user_agent = var.user_agent
  max_retries = var.max_retries
  backoff_factor = var.backoff_factor
  retry_on = var.retry_on
  timeout = var.timeout
  db_name = var.db_name
  db_table = var.db_table
  db_username = var.db_username
  db_password = var.db_password
}
