locals {
  airflow_port = 8080
  all_ips = ["0.0.0.0/0"]
}

resource "aws_launch_configuration" "launch_config" {
  image_id = "ami-0b69ea66ff7391e80"
  instance_type = var.instance_type
  security_groups = [aws_security_group.sg_airflow.id]
  user_data = data.template_file.user_data.rendered
  key_name = var.ec2_key_pair
  iam_instance_profile = data.terraform_remote_state.iam.outputs.airflow_profile

  lifecycle {
	  create_before_destroy = true
  }
}

data "template_file" "user_data" {
  template = file("${path.module}/templates/user_data.sh")

  vars = {
    s3_bucket = var.s3_bucket
    urls_s3_key = var.urls_s3_key
    user_agent = var.user_agent
    max_retries = var.max_retries
    backoff_factor = var.backoff_factor
    retry_on = var.retry_on
    timeout = var.timeout
    db_name = var.db_name
    db_table = var.db_table
    db_username = var.db_username
    db_password = var.db_password
    host = data.terraform_remote_state.database.outputs.address
    port = data.terraform_remote_state.database.outputs.port
    webserver_service = file("${path.module}/templates/airflow-webserver.service")
    scheduler_service = file("${path.module}/templates/airflow-scheduler.service")
  }
}

resource "aws_autoscaling_group" "asg_airflow" {
  launch_configuration = aws_launch_configuration.launch_config.name

  vpc_zone_identifier = [
    data.terraform_remote_state.network.outputs.public_subnet_1_id,
    data.terraform_remote_state.network.outputs.public_subnet_2_id
  ]

  min_size = 1
  max_size = 1

  tag {
    key = "Name"
    value = "${var.instance_name}-asg"
    propagate_at_launch = true
  }

  dynamic "tag" {
    for_each = var.custom_tags
    content {
      key = tag.key
      value = tag.value
      propagate_at_launch = true
    }
  }
}

resource "aws_security_group" "sg_airflow" {
  name = "${var.instance_name}-security-group"
  vpc_id = data.terraform_remote_state.network.outputs.vpc_id
}

resource "aws_security_group_rule" "access_to_airflow_webui" {
	security_group_id = aws_security_group.sg_airflow.id
  type = "ingress"
  from_port = local.airflow_port
  to_port = local.airflow_port
  protocol = "tcp"
  cidr_blocks = [var.my_ip] 
}

resource "aws_security_group_rule" "ssh_access" {
	security_group_id = aws_security_group.sg_airflow.id
  type = "ingress"
  from_port = 22
  to_port = 22
  protocol = "tcp"
  cidr_blocks = [var.my_ip]
}

# needed for yum
resource "aws_security_group_rule" "outbound" {
  security_group_id = aws_security_group.sg_airflow.id
  type = "egress"
  from_port = 0
  to_port = 0
  protocol = "-1"
  cidr_blocks = local.all_ips
}

data "terraform_remote_state" "database" {
  backend = "s3"
  config = {
    bucket = var.state_bucket
    key = var.db_remote_state_key
    region = var.region
  }
}

data "terraform_remote_state" "iam" {
  backend = "s3"
  config = {
    bucket = var.state_bucket
    key = var.iam_remote_state_key
    region = var.region
  }
}

data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = var.state_bucket
    key = var.network_remote_state_key
    region = var.region
  }
}
