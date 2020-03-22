output "address" {
  value       = module.data_warehouse.address
  description = "endpoint to connect to the database"
}

output "port" {
  value       = module.data_warehouse.port
  description = "port the database is listening on"
}
