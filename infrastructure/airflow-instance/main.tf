terraform {
  required_version = ">= 0.12, < 0.13"
  backend "s3" {
    key = "airflow-instance/terraform.tfstate"
  }
}

provider "aws" {
  version = "~> 2.0"
  region = var.region
  profile = var.aws_profile
}

module "airflow_instance" {
  source = "github.com/jschnab/terraform_modules//airflow-instance?ref=v0.0.4"

  instance_name = "airflow-instance"
  state_bucket = var.state_bucket
  region = var.region
  db_remote_state_key = "databases/rds/terraform.tfstate"
  iam_remote_state_key = "global/iam/terraform.tfstate"
  network_remote_state_key = "global/network/terraform.tfstate"
  instance_type = "t2.micro"
  custom_tags = {
    Owner = "Airflow"
    DeployedBy = "Terraform"
  }

  my_ip = var.my_ip
  ec2_key_pair = var.ec2_key_pair
  s3_bucket = var.data_bucket
  urls_s3_key = "input/scraping_links.txt"
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
