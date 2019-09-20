#!/bin/bash

YELLOWBOLD="\e[1;33m"
FILE_DIR=$(cd `dirname $0` && pwd)
INFRA_DIR=$(dirname -- "$(dirname $FILE_DIR)")/infrastructure

echo -e "\n${YELLOWBOLD}Deleting the SSH key pair..."
aws ec2 delete-key-pair \
    --key-name airflow-instance-ssh \
    --profile $TF_VAR_aws_profile
chmod 755 $HOME/.ssh/airflow-instance-ssh.pem
rm $HOME/.ssh/airflow-instance-ssh.pem

echo -e "\n${YELLOWBOLD}Destroying the Airflow EC2 instance...\n"
cd $INFRA_DIR/airflow-instance
terraform destroy -auto-approve

echo -e "\n${YELLOWBOLD}Destroying the database...\n"
cd $INFRA_DIR/databases/data_warehouse
terraform destroy -auto-approve

echo -e "\n${YELLOWBOLD}Destroying the VPC resources...\n"
cd $INFRA_DIR/global/network
terraform destroy -auto-approve

echo -e "\n${YELLOWBOLD}Destroying the IAM resources...\n"
cd $INFRA_DIR/global/iam
terraform destroy -auto-approve

echo -e "\n${YELLOWBOLD}Destroying the S3 buckets...\n"
cd $INFRA_DIR/global/s3
terraform destroy -auto-approve
