terraform {
  required_version = ">= 0.12, < 0.13"
  backend "s3" {
    key = "network/vpc/terraform.tfstate"
  }
}

provider "aws" {
  version = "~> 2.0"
  region  = var.region
  profile = var.aws_profile
}

module "network" {
  source      = "github.com/jschnab/terraform_modules//network/scraping_vpc?ref=v0.0.34"
  region      = var.region
  aws_profile = var.aws_profile
}
