terraform {
  required_version = ">= 0.12, < 0.13"
  backend "s3" {
    key = "airflow-instance/terraform.tfstate"
  }
}

provider "aws" {
  version = "~> 2.0"
  region  = var.region
  profile = var.aws_profile
}

module "airflow_instance" {
  source = "github.com/jschnab/terraform_modules//ec2/airflow?ref=v0.0.34"

  instance_name                    = "airflow"
  state_bucket                     = var.state_bucket
  region                           = var.region
  iam_remote_state_key             = "iam/terraform.tfstate"
  vpc_remote_state_key             = "network/vpc/terraform.tfstate"
  security_groups_remote_state_key = "network/security-groups/terraform.tfstate"
  metadata_db_remote_state_key     = "databases/airflow-metadata/terraform.tfstate"
  db_remote_state_key              = "databases/data-warehouse/terraform.tfstate"
  instance_type                    = "t2.micro"
  custom_tags = {
    DeployedBy = "Terraform"
  }
  ec2_key_pair      = var.airflow_key_pair
  s3_bucket         = var.data_bucket
  urls_s3_key       = "input/scraping_links.txt"
  user_agent        = var.user_agent
  max_retries       = var.max_retries
  backoff_factor    = var.backoff_factor
  retry_on          = var.retry_on
  timeout           = var.timeout
  db_name           = var.db_name
  db_table          = var.db_table
  db_username       = var.db_username
  db_password       = var.db_password
  remote_log_folder = var.remote_log_folder
  meta_db_password  = var.meta_db_password
}
