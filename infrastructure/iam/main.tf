terraform {
  required_version = ">= 0.12, < 0.13"
  backend "s3" {
    key = "iam/terraform.tfstate"
  }
}
  
provider "aws" {
  version = "~> 2.0"
  region = var.region
  profile = var.aws_profile
}

module "airflow_profile" {
	source = "github.com/jschnab/terraform_modules//iam/airflow_profile?ref=v0.0.19"
	aws_profile = var.aws_profile
	data_bucket = var.data_bucket
	region = var.region
}
