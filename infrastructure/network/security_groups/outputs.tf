output "database_security_group_id" {
  description = "ID of the database security group"
  value       = module.security_groups.database_security_group_id
}

output "ec2_security_group_id" {
  description = "ID of the EC2 instance security group"
  value       = module.security_groups.ec2_security_group_id
}

output "webserver_security_group_id" {
  description = "ID of the webserver security group"
  value       = module.security_groups.webserver_security_group_id
}

output "load_balancer_security_group_id" {
  description = "ID of the load balancer security group"
  value       = module.security_groups.load_balancer_security_group_id
}
