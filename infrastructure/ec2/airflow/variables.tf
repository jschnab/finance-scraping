variable "aws_profile" {
  description = "AWS profile to use when provisioning the infrastructure"
  type        = string
}

variable "region" {
  description = "AWS region where the infrastructure is built"
  type        = string
}

variable "my_ip" {
  description = "IP address allowed to access the Airflow instance"
  type        = string
}

variable "airflow_key_pair" {
  description = "key pair to SSH into the Airflow instance"
  type        = string
}

variable "state_bucket" {
  description = "S3 bucket where Terraform state is stored"
  type        = string
}

variable "data_bucket" {
  description = "S3 bucket where data is stored"
  type        = string
}

variable "user_agent" {
  description = "user agent to use for web scraping"
  type        = string
}

variable "max_retries" {
  description = "maximum number of retries if web scraping fails"
  type        = number
}

variable "backoff_factor" {
  description = "backoff factor value for web scraping"
  type        = number
}

variable "retry_on" {
  description = "comma-separated series of HTTP code to retry scraping on"
  type        = string
}

variable "timeout" {
  description = "timeout value (seconds) for web scraping"
  type        = number
}

variable "db_name" {
  description = "name of the database to store data in the RDS instance"
  type        = string
}

variable "db_table" {
  description = "name of the table to store data in the RDS instance"
  type        = string
}

variable "db_username" {
  description = "username to access the RDS instance"
  type        = string
}

variable "db_password" {
  description = "password to access the RDS instance"
  type        = string
}

variable "remote_log_folder" {
  description = "remote S3 bucket where to store Airflow logs"
  type        = string
}

variable "meta_db_password" {
  description = "password to access the Airflow metadata database"
  type        = string
}
