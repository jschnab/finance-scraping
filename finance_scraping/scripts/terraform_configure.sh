#!/bin/bash

YELLOWBOLD="\e[1;33m"
NORMAL="\e[0m"

# exit the script if one command fails
set -e

# we set variables useful for Terraform in a file
ENV_FILE=~/.bash_non_interactive
if [[ ! -f ~/.bash_non_interactive ]]; then
    touch $ENV_FILE
fi

echo -e "${YELLOWBOLD}\nWelcome to the configuration of the web scraping utility!${NORMAL}"

# check the AWS command-line interface is installed, install if not
if ! [[ -x "$(command -v aws)" ]]; then
    echo "aws-cli is not installed, installing..."
    /usr/bin/pip3 install --upgrade --user --yes aws-cli
    echo "export PATH=$HOME/.local/bin:$PATH" >> $ENV_FILE
fi

# record the user's IP address to later add it to an AWS security group in with Terraform
MYIP=`dig +short myip.opendns.com @resolver1.opendns.com`
VAR="TF_VAR_my_ip"
if [[ ! -z $VAR ]]; then
  sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=${MYIP}/32" >> $ENV_FILE

# set Terraform environment variables from user's input
declare -a PARAMS=(aws_profile region user_agent max_retries backoff_factor \
	retry_on timeout db_username db_password)

echo -e "\n${YELLOWBOLD}Please enter configuration values:${NORMAL} \n"

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

# put the key-pair name in an environment variable to later add it to a load balancer
# launch config with Terraform
VAR="TF_VAR_ec2_key_pair"
if [[ ! -z $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=airflow-instance-ssh" >> $ENV_FILE

# set S3 buckets names as Terraform environment variables
RANDOM_STR=$(head /dev/urandom | tr -dc a-z | head -c 20)
VAR="TF_VAR_state_bucket"
if [[ ! -z $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=terraform-state-$RANDOM_STR" >> $ENV_FILE

VAR="TF_VAR_data_bucket"
if [[ ! -z $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=finance-scraping-$RANDOM_STR" >> $ENV_FILE

VAR="TF_VAR_remote_log_folder"
if [[ ! -z $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=airflow-logs-$RANDOM_STR" >> $ENV_FILE

# set Airflow metadata database password
META_DB_PASSWORD=$(head /dev/urandom | tr -dc a-z0-9 | head -c 20)
VAR="TF_VAR_meta_db_password"
if [[ ! -z $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=$META_DB_PASSWORD" >> $ENV_FILE

# set database and table names as Terraform environment variables
VAR="TF_VAR_db_name"
if [[ ! -z $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=finance_scraping" >> $ENV_FILE

VAR="TF_VAR_db_table"
if [[ ! -z $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=security_report" >> $ENV_FILE

echo -e "${YELLOWBOLD}Configuration is finished.${NORMAL}"
