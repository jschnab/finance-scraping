terraform {
  required_version = ">= 0.12, < 0.13"
  backend "s3" {
    key = "global/iam/terraform.tfstate"
  }
}
  
provider "aws" {
  version = "~> 2.0"
  region = "us-east-1"
  profile = var.aws_profile
}

# document which defines the instance role
data "aws_iam_policy_document" "assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

# document which defines the policy we will attach to the instance role
data "aws_iam_policy_document" "airflow_policy_document" {
  statement {
    sid = "ListObjectBucket"
    effect = "Allow"  
    actions = ["s3:ListBucket"]
    resources = ["arn:aws:s3:::${var.data_bucket}"]
  }

  statement {
    sid = "AllowObjectActions"
    effect = "Allow"
    actions = ["s3:*Object"]
    resources = ["arn:aws:s3:::${var.data_bucket}/*"]
  }

  statement {
    sid = "RDSFullAccess"
    effect = "Allow"
    actions = ["rds:*"]
    resources = ["arn:aws:rds:us-east-1:*:*"]
  }

  statement {
    sid = "RDSDescribeAll"
    effect = "Allow"
    actions = ["rds:Describe*"]
    resources = ["*"]
  }
}

# step 1: we create a role
resource "aws_iam_role" "airflow_role" {
  name = "airflow_role"
  assume_role_policy = "${data.aws_iam_policy_document.assume_role.json}"
}

# step 2: we create a policy
resource "aws_iam_policy" "airflow_policy" {
  name = "airflow_policy"
  policy = "${data.aws_iam_policy_document.airflow_policy_document.json}"
}

# step 3: we attach the role to the policy
resource "aws_iam_role_policy_attachment" "airflow_role_policy_attach" {
  role = "${aws_iam_role.airflow_role.name}"
  policy_arn = "${aws_iam_policy.airflow_policy.arn}"
}

# step4: we create an instance profile from the role defined at step 1
resource "aws_iam_instance_profile" "airflow_profile" {
  name = "airflow_profile"
  role = "${aws_iam_role.airflow_role.name}"
}
