variable "aws_profile" {
  description = "AWS profile to use to build the infrastructure"
  type        = string
}

variable "region" {
  description = "AWS region where infrastructure is build"
  type        = string
}

variable "db_name" {
  description = "name of the database in the instance"
  type        = string
}

variable "meta_db_password" {
  description = "password for Postgres database"
  type        = string
}

variable "state_bucket" {
  description = "name of the S3 bucket where remote state is stored"
  type        = string
}
