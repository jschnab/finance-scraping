terraform {
  required_version = ">= 0.12, < 0.13"

  # we only provide the key, bucket and region are provided
  # through the backend configuration file
  backend "s3" {
    key = "databases/airflow-metadata/terraform.tfstate"
  }
}

provider "aws" {
  version = "~> 2.0"
  region  = var.region
  profile = var.aws_profile
}

module "airflow_metadata" {
  source                           = "github.com/jschnab/terraform_modules//databases/rds?ref=v0.0.34"
  db_name                          = "airflow"
  db_username                      = "airflow"
  db_password                      = var.meta_db_password
  region                           = var.region
  aws_profile                      = var.aws_profile
  state_bucket                     = var.state_bucket
  vpc_remote_state_key             = "network/vpc/terraform.tfstate"
  security_groups_remote_state_key = "network/security-groups/terraform.tfstate"
  subnet_group_name                = "airflow-metadata-db-subnet-group"
}
