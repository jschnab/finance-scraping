output "address" {
  value       = module.airflow_metadata.address
  description = "endpoint to connect to the database"
}

output "port" {
  value       = module.airflow_metadata.port
  description = "port the database is listening on"
}
