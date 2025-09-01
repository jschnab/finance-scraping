output "airflow_profile" {
  description = "IAM profile for the Airflow instance"
  value       = module.airflow_profile.airflow_profile
}

output "webserver_profile" {
  description = "IAM profile for the webserver instances"
  value       = module.webserver_profile.webserver_profile
}
