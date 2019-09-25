variable "region" {
  description = "AWS region where to build infrastructure"
  type = string
}

variable "aws_profile" {
  description = "AWS profile Terraform should use"
  type = string
}

variable "data_bucket" {
  description = "AWS S3 bucket where scraped data is stored"
  type = string
}

variable "state_bucket" {
  description = "AWS S3 bucket where Terraform state is stored"
  type = string
}

variable "logs_bucket" {
	description = "AWS S3 bucket where Airflow write logs"
	type = string
}
