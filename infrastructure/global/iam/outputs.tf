output "airflow_profile" {
  description = "IAM profile for the Airflow instance"
  value = module.airflow_profile.airflow_profile
}
