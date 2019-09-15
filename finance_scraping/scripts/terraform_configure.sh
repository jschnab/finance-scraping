#!/bin/bash

ENV_FILE=~/.bashrc

echo "Welcome to the configuration of the web scraping utility!"

# check the AWS command-line interface is installed, install if not
if ! [[ -x "$(command -v aws)" ]]; then
    echo "aws-cli is not installed, installing..."
    /usr/bin/pip3 install --upgrade --user --yes aws-cli
    echo "export PATH=$HOME/.local/bin:$PATH" >> $ENV_FILE
fi

# check jq (JSON parsing) is installed, install if not
if ! [[ -x "$(command -v jq)" ]]; then
    echo "jq (JSON parsing tool) is not installed, installing..."
    sudo apt install -y jq
fi

# create a key-pair to later SSH into the Airflow instance
echo "creating key pair 'airflow-instance-ssh' and saving in $HOME/.ssh"
KEY_PAIR=$(aws ec2 create-key-pair --key-name airflow-instance-ssh 2>/dev/null)
if [[ -z $KEY_PAIR ]]; then
    echo
    echo "The key pair 'airflow-instance-ssh' already exists or there was a problem during key creation."
    echo "Please make sure you actually have this key pair, or restart configuration."
    echo "Press any key to continue..."
    echo
    read
else
    echo $KEY_PAIR | jq '.KeyMaterial' > $HOME/.ssh/airflow-instance-ssh.pem
fi

# put the key-pair name in an environment variable to later add it to a load balancer launch config with Terraform
VAR="TF_VAR_ec2_key_pair"
if [[ ! -z $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=airflow-instance-ssh" >> $ENV_FILE

# record the user's IP address to later add it to an AWS security group in with Terraform
MYIP=`dig +short myip.opendns.com @resolver1.opendns.com`
VAR="TF_VAR_my_ip"
if [[ ! -z $VAR ]]; then
  sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=${MYIP}/32" >> $ENV_FILE

# set Terraform environment variables from user's input
declare -a PARAMS=(data_bucket aws_profile urls_s3_key user_agent max_retries \
    backoff_factor retry_on timeout db_name db_table db_username db_password \
    state_bucket)

echo
echo "Please enter configuration values: "
echo

# loop through parameters
for ((i=0; i<${#PARAMS[@]}; i++)); do

    # show the existing value to the user
    VAR="TF_VAR_${PARAMS[i]}"
    EXISTING=`cat $ENV_FILE | grep $VAR | cut -d= -f2`
    echo "${PARAMS[i]}[$EXISTING]: "
    read VAL

    # keep waiting for user's input if no value is set
    while [[ -z ${VAL} ]] && [[ -z $EXISTING ]]; do
	echo "${PARAMS[i]}[$EXISTING]: "
	read VAL
    done

    # user's input overwrites the existing variable
    if [[ ! -z ${VAL} ]]; then
	sed -i "/^export $VAR/d" $ENV_FILE
	echo "export $VAR=$VAL" >> $ENV_FILE
    fi
done

source $ENV_FILE

echo "Configuration is finished."
