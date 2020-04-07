#!/bin/bash

set -e

YELLOWBOLD="\e[1;33m"

FILE_DIR=$(cd "$(dirname "$0")" && pwd)
INFRA_DIR=$(dirname -- "$(dirname "$FILE_DIR")")/infrastructure

source ~/.terraform_env_vars

# create a key-pair to SSH into the Airflow instance
if [[ ! -f ~/.ssh/$TF_VAR_airflow_key_pair.pem ]]; then
    echo -e "\n${YELLOWBOLD}Creating key pair '$TF_VAR_airflow_key_pair' and saving in $HOME/.ssh${NORMAL}"
    aws ec2 create-key-pair --key-name "$TF_VAR_airflow_key_pair" \
        --query 'KeyMaterial' \
        --output text \
        --profile "$TF_VAR_aws_profile" \
        > ~/.ssh/"$TF_VAR_airflow_key_pair".pem
    chmod 400 ~/.ssh/"$TF_VAR_airflow_key_pair".pem
fi

# create a key-pair to SSH into the webserver instance
if [[ ! -f ~/.ssh/$TF_VAR_webserver_key_pair.pem ]]; then
    echo -e "\n${YELLOWBOLD}Creating key pair '$TF_VAR_webserver_key_pair' and saving in $HOME/.ssh${NORMAL}"
    aws ec2 create-key-pair --key-name "$TF_VAR_webserver_key_pair" \
        --query 'KeyMaterial' \
        --output text \
        --profile "$TF_VAR_aws_profile" \
        > ~/.ssh/"$TF_VAR_webserver_key_pair".pem
    chmod 400 ~/.ssh/"$TF_VAR_webserver_key_pair".pem
fi

# add state bucket to backend configuration file
if [[ -n $(grep "^bucket =" "$INFRA_DIR"/backend.hcl) ]]; then
    sed -i "/^bucket =/d" "$INFRA_DIR"/backend.hcl
fi
echo "bucket = \"$TF_VAR_state_bucket\"" >> "$INFRA_DIR"/backend.hcl

# add AWS region to backend configuration file
if [[ -n $(grep "^region =" "$INFRA_DIR"/backend.hcl) ]]; then
    sed -i "/^region =/d" "$INFRA_DIR"/backend.hcl
fi
echo "region = \"$TF_VAR_region\"" >> "$INFRA_DIR"/backend.hcl

# build the global infrastructure : S3, IAM and VPC
cd "$INFRA_DIR"/s3
echo -e "\n${YELLOWBOLD}Building S3 buckets...\n"
terraform init 
terraform apply -auto-approve
# send the file containing the list of scraping links to the S3 bucket
cd "$FILE_DIR"
aws s3api put-object \
	--bucket "$TF_VAR_data_bucket" \
	--key input/scraping_links.txt \
	--body ../scraping_links.txt \
	--profile "$TF_VAR_aws_profile" \
	>/dev/null

cd "$INFRA_DIR"/iam
echo -e "\n${YELLOWBOLD}Building IAM resources..\n"
terraform init -backend-config="$INFRA_DIR"/backend.hcl
terraform apply -auto-approve

cd "$INFRA_DIR"/network/vpc
echo -e "\n${YELLOWBOLD}Building VPC resources...\n"
terraform init -backend-config="$INFRA_DIR"/backend.hcl
terraform apply -auto-approve

cd "$INFRA_DIR"/network/security_groups
echo -e "\n${YELLOWBOLD}Building security groups...\n"
terraform init -backend-config="$INFRA_DIR"/backend.hcl
terraform apply -auto-approve

# build the RDS instances
cd "$INFRA_DIR"/databases/data_warehouse
echo -e "\n${YELLOWBOLD}Building the data warehouse...\n"
terraform init -backend-config="$INFRA_DIR"/backend.hcl
terraform apply -auto-approve

cd "$INFRA_DIR"/databases/airflow_metadata
echo -e "\n${YELLOWBOLD}Building the Airflow metadata database...\n"
terraform init -backend-config="$INFRA_DIR"/backend.hcl
terraform apply -auto-approve

# build the EC2 instance running Apache Airflow
cd "$INFRA_DIR"/ec2/airflow
echo -e "\n${YELLOWBOLD}Building the Airflow instance...\n"
terraform init -backend-config="$INFRA_DIR"/backend.hcl
terraform apply -auto-approve

# build the EC2 instance running the dashboard webserver
cd "$INFRA_DIR"/ec2/webserver
echo -e "\n${YELLOWBOLD}Building the dashboard webserver...\n"
terraform init -backend-config="$INFRA_DIR"/backend.hcl
terraform apply -auto-approve
