terraform {
  required_version = ">= 0.12, < 0.13"
}

provider "aws" {
  version = "~> 2.0"
  region = "us-east-1"
  profile = var.aws_profile
}

resource "aws_s3_bucket" "terraform_state" {
		bucket = var.state_bucket

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket" "finance_scraping" {
  bucket = var.data_bucket

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
