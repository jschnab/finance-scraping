#!/bin/bash

FILE_DIR=$(cd `dirname $0` && pwd)
INFRA_DIR=$(dirname -- "$(dirname $FILE_DIR)")/infrastructure

# build the global infrastructure : S3, IAM and VPC
cd $INFRA_DIR/global/s3
terraform init 
terraform apply -auto-approve
cd $FILE_DIR
aws s3api put-object --bucket $TF_VAR_data_bucket --key $TF_VAR_urls_s3_key --body ../scraping_links.txt

cd $INFRA_DIR/global/iam
terraform init -backend-config=$INFRA_DIR/backend.hcl
terraform apply -auto-approve

cd $INFRA_DIR/global/network
terraform init -backend-config=$INFRA_DIR/backend.hcl
terraform apply -auto-approve

# build the RDS instance
cd $INFRA_DIR/database/data_warehouse
terraform init -backend-config=$INFRA_DIR/backend.hcl
terraform apply -auto-approve

# build the EC2 instance running Apache Airflow
cd $INFRA_DIR/airflow-instance
terraform init -backend-config=$INFRA_DIR/backend.hcl
terraform apply -auto-approve