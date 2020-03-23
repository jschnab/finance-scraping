variable "my_ip" {
  description = "IP address allowed to connect to the Airflow instance"
  type        = string
}

variable "state_bucket" {
  description = "S3 bucket where Terraform remote state is stored"
  type        = string
}

variable "region" {
  description = "region where to desploy the infrastructure"
  type        = string
}

variable "aws_profile" {
  description = "AWS region where to deploy the infrastructure"
  type        = string
}
