#!/bin/bash

set -e

YELLOWBOLD="\e[1;33m"
FILE_DIR=$(cd `dirname $0` && pwd)
INFRA_DIR=$(dirname -- "$(dirname $FILE_DIR)")/infrastructure

echo -e "\n${YELLOWBOLD}Deleting the SSH key pair..."
aws ec2 delete-key-pair \
    --key-name airflow-instance-ssh \
    --profile $TF_VAR_aws_profile
chmod 755 $HOME/.ssh/airflow-instance-ssh.pem
rm $HOME/.ssh/airflow-instance-ssh.pem

echo -e "\n${YELLOWBOLD}Destroying Airflow EC2 instance...\n"
cd $INFRA_DIR/ec2/airflow-instance
terraform destroy -auto-approve
rm -rf $INFRA_DIR/ec2/airflow-instance/.terraform

echo -e "\n${YELLOWBOLD}Destroying the data warehouse...\n"
cd $INFRA_DIR/databases/data_warehouse
terraform destroy -auto-approve
rm -rf $INFRA_DIR/databases/data_warehouse/.terraform

echo -e "\n${YELLOWBOLD}Destroying the metadata database...\n"
cd $INFRA_DIR/databases/airflow_metadata
terraform destroy -auto-approve
rm -rf $INFRA_DIR/databases/airflow_metadata/.terraform

echo -e "\n${YELLOWBOLD}Destroying security groups...\n"
cd $INFRA_DIR/network/security_groups
terraform destroy -auto-approve
rm -rf $INFRA_DIR/network/security_groups/.terraform

echo -e "\n${YELLOWBOLD}Destroying VPC resources...\n"
cd $INFRA_DIR/network/vpc
terraform destroy -auto-approve

echo -e "\n${YELLOWBOLD}Destroying IAM resources...\n"
cd $INFRA_DIR/iam
terraform destroy -auto-approve
rm -rf $INFRA_DIR/iam/.terraform

echo -e "\n${YELLOWBOLD}Destroying S3 buckets...\n"
cd $INFRA_DIR/s3
terraform destroy -auto-approve
