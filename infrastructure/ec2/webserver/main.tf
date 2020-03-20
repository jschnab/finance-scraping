terraform {
  required_version = ">= 0.12, < 0.13"
  backend "s3" {
    key = "webserver/terraform.tfstate"
  }
}

provider "aws" {
  version = "~> 2.0"
  region  = var.region
  profile = var.profile
}

module "webserver" {
  source                    = "~/terraform_projects/terraform_modules/ec2/webserver"
  key_name                  = "webserver-ssh-key"
  state_bucket              = var.state_bucket
  user_data                 = data.template_file.user_data.rendered
  state_security_groups_key = "network/security_groups/terraform.tfstate"
  state_iam_key             = "iam/terraform.tfstate"
  region                    = var.region
}
