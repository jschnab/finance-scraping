terraform {
  required_version = ">= 0.12, < 0.13"
}

provider "aws" {
  version = "~> 2.0"
  region = var.region
  profile = var.aws_profile
}

module "buckets" {
	source = "github.com/jschnab/terraform_modules//s3/state_data_logs?ref=v0.0.8"
	state_bucket = var.state_bucket
	data_bucket = var.data_bucket
	logs_bucket = var.logs_bucket
}
