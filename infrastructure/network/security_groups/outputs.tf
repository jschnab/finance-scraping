output "database_security_group_id" {
	description = "ID of the database security group"
	value = module.security_groups.database_security_group_id
}

output "ec2_security_group_id" {
	description = "ID of the EC2 instance security group"
	value = module.security_groups.ec2_security_group_id
}
