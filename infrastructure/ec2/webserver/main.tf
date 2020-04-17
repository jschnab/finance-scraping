terraform {
  required_version = ">= 0.12, < 0.13"
  backend "s3" {
    key = "webserver/terraform.tfstate"
  }
}

provider "aws" {
  version = "~> 2.0"
  region  = var.region
  profile = var.aws_profile
}

module "webserver" {
  source                    = "github.com/jschnab/terraform_modules//ec2/webserver?ref=v0.0.34"
  key_name                  = "webserver-instance-ssh"
  state_bucket              = var.state_bucket
  user_data                 = data.template_file.user_data.rendered
  state_security_groups_key = "network/security-groups/terraform.tfstate"
  state_iam_key             = "iam/terraform.tfstate"
  state_vpc_key             = "network/vpc/terraform.tfstate"
  region                    = var.region
  domain_name               = var.domain_name
  custom_tags = {
    Name = "finance-webserver"
  }
}

data "template_file" "user_data" {
  template = file("${path.module}/templates/user_data.sh")
  vars = {
    nginx_conf       = data.template_file.nginx_conf.rendered
    gunicorn_service = data.template_file.gunicorn_service.rendered
    gunicorn_socket  = data.template_file.gunicorn_socket.rendered
    host             = data.terraform_remote_state.database.outputs.address
    port             = data.terraform_remote_state.database.outputs.port
    db_name          = var.db_name
    db_table         = var.db_table
    db_username      = var.db_username
    db_password      = var.db_password
  }
}

data "template_file" "nginx_conf" {
  template = file("${path.module}/templates/nginx_conf")
}

data "template_file" "gunicorn_service" {
  template = file("${path.module}/templates/gunicorn_service")
}

data "template_file" "gunicorn_socket" {
  template = file("${path.module}/templates/gunicorn_socket")
}

data "terraform_remote_state" "database" {
  backend = "s3"
  config = {
    bucket = var.state_bucket
    region = var.region
    key    = "databases/data-warehouse/terraform.tfstate"
  }
}
