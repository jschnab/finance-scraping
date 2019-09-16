#!/bin/bash

YELLOWBOLD="\e[1;33m"

FILE_DIR=$(cd `dirname $0` && pwd)
INFRA_DIR=$(dirname -- "$(dirname $FILE_DIR)")/infrastructure

# add state bucket to backend configuration file
if [[ ! -z $(grep "^bucket =" $INFRA_DIR/backend.hcl) ]]; then
    sed -i "/^bucket =/d" $INFRA_DIR/backend.hcl
fi
echo "bucket = \"$TF_VAR_state_bucket\"" >> $INFRA_DIR/backend.hcl

# add AWS region to backend configuration file
if [[ ! -z $(grep "^region =" $INFRA_DIR/backend.hcl) ]]; then
    sed -i "/^region =/d" $INFRA_DIR/backend.hcl
fi
echo "region = \"$TF_VAR_region\"" >> $INFRA_DIR/backend.hcl

# build the global infrastructure : S3, IAM and VPC
cd $INFRA_DIR/global/s3
echo -e "\n${YELLOWBOLD}Building S3 buckets..."
terraform init 
terraform apply -auto-approve
cd $FILE_DIR
aws s3api put-object \
	--bucket $TF_VAR_data_bucket \
	--key $TF_VAR_urls_s3_key \
	--body ../scraping_links.txt \
	--profile $TF_VAR_aws_profile
	>/dev/null

cd $INFRA_DIR/global/iam
echo -e "\n${YELLOWBOLD}Building IAM resources.."
terraform init -backend-config=$INFRA_DIR/backend.hcl
terraform apply -auto-approve

cd $INFRA_DIR/global/network
echo -e "\n${YELLOWBOLD}Building VPC resources..."
terraform init -backend-config=$INFRA_DIR/backend.hcl
terraform apply -auto-approve

# build the RDS instance
cd $INFRA_DIR/databases/data_warehouse
echo -e "\n${YELLOWBOLD}Building the database..."
terraform init -backend-config=$INFRA_DIR/backend.hcl
terraform apply -auto-approve

# build the EC2 instance running Apache Airflow
cd $INFRA_DIR/airflow-instance
echo -e "\n${YELLOWBOLD}Building the Airflow instance...\n"
terraform init -backend-config=$INFRA_DIR/backend.hcl
terraform apply -auto-approve
