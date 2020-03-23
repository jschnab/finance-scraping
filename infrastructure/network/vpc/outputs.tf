output "private_subnet_1_id" {
  description = "ID of private subnet 1"
  value       = module.network.private_subnet_1_id
}

output "private_subnet_2_id" {
  description = "ID of private subnet 2"
  value       = module.network.private_subnet_2_id
}

output "public_subnet_1_id" {
  description = "ID of public subnet 1"
  value       = module.network.public_subnet_1_id
}

output "public_subnet_2_id" {
  description = "ID of public subnet 2"
  value       = module.network.public_subnet_2_id
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = module.network.vpc_id
}
