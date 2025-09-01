output "state_bucket_arn" {
  value       = module.buckets.state_bucket_arn
  description = "ARN of the S3 bucket storing Terraform state"
}

output "data_bucket_arn" {
  value       = module.buckets.data_bucket_arn
  description = "ARN of bucket storing scraped data"
}

output "remote_folder_arn" {
  value       = module.buckets.logs_bucket_arn
  description = "ARN of bucket storing Airflow logs"
}
