terraform {
  required_version = ">= 0.12, < 0.13"
  backend "s3" {
    key = "global/network/terraform.tfstate"
  }
}

provider "aws" {
  version = "~> 2.0"
  region = var.region
  profile = var.aws_profile
}

resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "finance-scraping-vpc"
  }
}

data "aws_vpc_endpoint_service" "s3" {
  service = "s3"
}

resource "aws_vpc_endpoint" "s3_endpoint" {
  vpc_id = aws_vpc.vpc.id
  service_name = data.aws_vpc_endpoint_service.s3.service_name
  tags = { Name = "s3-endpoint" }
}

resource "aws_subnet" "public_1" {
  availability_zone = "${var.region}a"
  vpc_id = aws_vpc.vpc.id
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = true
  tags = { Name = "public-subnet-1" }
}

resource "aws_subnet" "public_2" {
  availability_zone = "${var.region}b"
  vpc_id = aws_vpc.vpc.id
  cidr_block = "10.0.2.0/24"
  map_public_ip_on_launch = true
  tags = { Name = "public-subnet-2" }
}

resource "aws_subnet" "private_1" {
  availability_zone = "${var.region}a"
  vpc_id = aws_vpc.vpc.id
  cidr_block = "10.0.3.0/24"
  tags = { Name = "private-subnet-1" }
}

resource "aws_subnet" "private_2" {
  availability_zone = "${var.region}b"
  vpc_id = aws_vpc.vpc.id
  cidr_block = "10.0.4.0/24"
  tags = { Name = "private-subnet-2" }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id
  tags = { Name = "scraping-igw" }
}

resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = { Name = "public-route-table" }
}

resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.vpc.id

  tags = { Name = "private-route-table" }
}

resource "aws_route_table_association" "public_assoc_1" {
  subnet_id = aws_subnet.public_1.id
  route_table_id = aws_route_table.public_route_table.id
}

resource "aws_route_table_association" "public_assoc_2" {
  subnet_id = aws_subnet.public_2.id
  route_table_id = aws_route_table.public_route_table.id
}

resource "aws_route_table_association" "private_assoc_1" {
  subnet_id = aws_subnet.private_1.id
  route_table_id = aws_route_table.private_route_table.id
}

resource "aws_route_table_association" "private_assoc_2" {
  subnet_id = aws_subnet.private_2.id
  route_table_id = aws_route_table.private_route_table.id
}

resource "aws_vpc_endpoint_route_table_association" "end_pub_assoc" {
  route_table_id = aws_route_table.public_route_table.id
  vpc_endpoint_id = aws_vpc_endpoint.s3_endpoint.id
}

resource "aws_vpc_endpoint_route_table_association" "end_priv_assoc" {
  route_table_id = aws_route_table.private_route_table.id
  vpc_endpoint_id = aws_vpc_endpoint.s3_endpoint.id
}
