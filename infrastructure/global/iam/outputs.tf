output "airflow_profile" {
  description = "IAM profile for the Airflow instance"
  value = aws_iam_instance_profile.airflow_profile.name
}
