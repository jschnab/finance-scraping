output "state_bucket_arn" {
  value = module.buckets.state_bucket_arn
  description = "ARN of the S3 bucket"
}

output "data_bucket_arn" {
  value = module.buckets.data_bucket_arn
  description = "ARN of bucket storing data"
}
