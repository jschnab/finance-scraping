variable "region" {
  description = "Region where the infrastructure should be built"
  type        = string
}

variable "aws_profile" {
  description = "Role to use when provisioning the infrastructure"
  type        = string
}

variable "state_bucket" {
  description = "AWS S3 bucket where Terraform state is stored"
  type        = string
}

variable "db_name" {
  description = "Name of the database in the RDS instance"
  type        = string
}

variable "db_table" {
  description = "Name of the table in the database"
  type        = string
}

variable "db_username" {
  description = "RDS instance credentials"
  type        = string
}

variable "db_password" {
  description = "RDS credentials"
  type        = string
}

variable "domain_name" {
  description = "Name of the web domain to use for the server"
  type        = string
}
