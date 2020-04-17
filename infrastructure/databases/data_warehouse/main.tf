terraform {
  required_version = ">= 0.12, < 0.13"

  # we only provide the key, bucket and region are provided
  # through the backend configuration file
  backend "s3" {
    key = "databases/data-warehouse/terraform.tfstate"
  }
}

provider "aws" {
  version = "~> 2.0"
  region  = var.region
  profile = var.aws_profile
}

module "data_warehouse" {
  source                           = "github.com/jschnab/terraform_modules//databases/rds?ref=v0.0.34"
  subnet_group_name                = "datawarehouse-subnet-group"
  db_name                          = var.db_name
  db_username                      = var.db_username
  db_password                      = var.db_password
  region                           = var.region
  aws_profile                      = var.aws_profile
  state_bucket                     = var.state_bucket
  vpc_remote_state_key             = "network/vpc/terraform.tfstate"
  security_groups_remote_state_key = "network/security-groups/terraform.tfstate"
}
