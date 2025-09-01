terraform {
  required_version = ">= 0.12, < 0.13"
}

provider "aws" {
  version = "~> 2.0"
  region  = var.region
  profile = var.aws_profile
}

module "buckets" {
  source            = "github.com/jschnab/terraform_modules//s3/scraping_buckets?ref=v0.0.34"
  state_bucket      = var.state_bucket
  data_bucket       = var.data_bucket
  remote_log_folder = var.remote_log_folder
}
