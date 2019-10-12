terraform {
	required_version = ">= 0.12, < 0.13"
	backend "s3" {
		key = "network/security_groups/terraform.tfstate"
	}
}

provider "aws" {
	version = "~> 2.0"
	region = var.region
	profile = var.aws_profile
}

module "security_groups" {
	source = "github.com/jschnab/terraform_modules//network/security-groups-ec2-rds?ref=v0.0.28"
	instance_name = "airflow-instance"
	web_port = 8080
	db_port = 5432
	my_ip = var.my_ip
	state_bucket = var.state_bucket
	region = var.region
	vpc_remote_state_key = "network/vpc/terraform.tfstate"
}
