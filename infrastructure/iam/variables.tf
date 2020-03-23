variable "aws_profile" {
  description = "AWS profile Terraform uses to create the infrastructure"
  type        = string
}

variable "region" {
  description = "AWS region where to built infrastructure"
  type        = string
}

variable "data_bucket" {
  description = "S3 bucket where scraped finance data is stored"
  type        = string
}

variable "remote_log_folder" {
  description = "S3 bucket where Airflow logs are stored"
  type        = string
}
