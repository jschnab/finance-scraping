#!/bin/bash

YELLOWBOLD="\e[1;33m"
NORMAL="\e[0m"

# exit the script if one command fails
set -e

# we set variables useful for Terraform in a file
ENV_FILE=~/.terraform_env_vars
if [[ ! -f $ENV_FILE ]]; then
    touch $ENV_FILE
fi

echo -e "${YELLOWBOLD}\nWelcome to the configuration of the web scraping utility!${NORMAL}"

echo -e "\n${YELLOWBOLD}File '"$ENV_FILE"' is not empty and may contain your current configuration. Do you want to overwrite it? (y/n)${NORMAL}"
read -r VAL
if [[ "$VAL" != "y" ]]; then
    echo -e "${YELLOWBOLD}Exiting${NORMAL}"
    exit
fi

# record the user's IP address to later add it to an AWS security group in with Terraform
MYIP=$(dig +short myip.opendns.com @resolver1.opendns.com)
VAR="TF_VAR_my_ip"
if [[ -n $VAR ]]; then
  sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=${MYIP}" >> $ENV_FILE

# set Terraform environment variables from user's input
declare -a PARAMS=(aws_profile region user_agent max_retries backoff_factor \
	retry_on timeout db_username db_password domain_name)

echo -e "\n${YELLOWBOLD}Please enter configuration values:${NORMAL} \n"

# loop through parameters
for ((i=0; i<${#PARAMS[@]}; i++)); do

    # show the existing value to the user
    VAR="TF_VAR_${PARAMS[i]}"
    EXISTING=$(grep "$VAR" "$ENV_FILE" | cut -d= -f2)
    echo "${PARAMS[i]}[$EXISTING]: "
    read -r VAL

    # keep waiting for user's input if no value is set
    while [[ -z ${VAL} ]] && [[ -z $EXISTING ]]; do
	echo "${PARAMS[i]}[$EXISTING]: "
	read -r VAL
    done

    # user's input overwrites the existing variable
    if [[ -n ${VAL} ]]; then
	sed -i "/^export $VAR/d" $ENV_FILE
	echo "export $VAR=$VAL" >> $ENV_FILE
    fi
done

# put the key-pair names in an environment variable to later add it
# to a load balancer launch config with Terraform
VAR="TF_VAR_airflow_key_pair"
if [[ -n $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=airflow-instance-ssh" >> $ENV_FILE

VAR="TF_VAR_webserver_key_pair"
if [[ -n $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=webserver-instance-ssh" >> $ENV_FILE

# set S3 buckets names as Terraform environment variables
# S3 buckets must have unique names
RANDOM_STR=$(head /dev/urandom | tr -dc '[:lower:]' | head -c 20)
VAR="TF_VAR_state_bucket"
if [[ -n $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=terraform-state-$RANDOM_STR" >> $ENV_FILE

VAR="TF_VAR_data_bucket"
if [[ -n $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=finance-scraping-$RANDOM_STR" >> $ENV_FILE

VAR="TF_VAR_remote_log_folder"
if [[ -n $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=airflow-logs-$RANDOM_STR" >> $ENV_FILE

# set Airflow metadata database password
META_DB_PASSWORD=$(head /dev/urandom | tr -dc a-z0-9 | head -c 20)
VAR="TF_VAR_meta_db_password"
if [[ -n $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=$META_DB_PASSWORD" >> $ENV_FILE

# set database and table names as Terraform environment variables
VAR="TF_VAR_db_name"
if [[ -n $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=finance_scraping" >> $ENV_FILE

VAR="TF_VAR_db_table"
if [[ -n $VAR ]]; then
    sed -i "/^export $VAR/d" $ENV_FILE
fi
echo "export $VAR=security_report" >> $ENV_FILE

echo -e "${YELLOWBOLD}Configuration is finished.${NORMAL}"
