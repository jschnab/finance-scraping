terraform {
  required_version = ">= 0.12, < 0.13"
  backend "s3" {
    key = "network/security-groups/terraform.tfstate"
  }
}

provider "aws" {
  version = "~> 2.0"
  region  = var.region
  profile = var.aws_profile
}

module "security_groups" {
  source                 = "github.com/jschnab/terraform_modules//network/scraping_security_groups?ref=v0.0.34"
  instance_name          = "airflow"
  airflow_webserver_port = 8080
  db_port                = 5432
  my_ip                  = "${var.my_ip}/32"
  state_bucket           = var.state_bucket
  region                 = var.region
  vpc_remote_state_key   = "network/vpc/terraform.tfstate"
}
