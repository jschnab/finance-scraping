#!/bin/bash

set -ex

exec > >(tee /var/log/user-data.log | logger -t user-data) 2>&1
echo BEGIN
date "+%Y-%m-%d %H:%M:%S"

yum install -y tree git python3 gcc postgresql-devel python3-devel.x86_64

# add user arguments are different on RedHat and Debian systems
# here for RedHat
adduser airflow

AIRFLOW_HOME=/home/airflow
AIRFLOW_ENV=$AIRFLOW_HOME/airflow.env
AIRFLOW_BIN=/usr/local/bin/airflow

# configure Airflow for management by systemd
SYSTEMD_DIR=/etc/systemd/system
cat << EOL >> $SYSTEMD_DIR/airflow-webserver.service
${webserver_service} 
EOL

cat << EOL >> $SYSTEMD_DIR/airflow-scheduler.service
${scheduler_service}
EOL

cat << EOL >> $AIRFLOW_ENV
AIRFLOW_HOME=$AIRFLOW_HOME
AIRFLOW_CONFIG=$AIRFLOW_HOME/airflow.cfg
FINANCE_SCRAPING_dag_start_date=$(date -d "yesterday 22:00" -u -Iminutes)
FINANCE_SCRAPING_s3_bucket=${s3_bucket}
FINANCE_SCRAPING_aws_profile=None
FINANCE_SCRAPING_urls_s3_key=${urls_s3_key}
FINANCE_SCRAPING_user_agent="${user_agent}"
FINANCE_SCRAPING_max_retries=${max_retries}
FINANCE_SCRAPING_backoff_factor=${backoff_factor}
FINANCE_SCRAPING_retry_on=${retry_on}
FINANCE_SCRAPING_timeout=${timeout}
FINANCE_SCRAPING_host=${host}
FINANCE_SCRAPING_port=${port}
FINANCE_SCRAPING_db_username=${db_username}
FINANCE_SCRAPING_db_password=${db_password}
FINANCE_SCRAPING_db_name=${db_name}
FINANCE_SCRAPING_db_table=${db_table}
EOL

set -a
source $AIRFLOW_ENV
set +a

cat << EOL >> $AIRFLOW_HOME/.bashrc
export FINANCE_SCRAPING_dag_start_date=$(date -d "yesterday 22:00" -u -Iminutes)
export FINANCE_SCRAPING_s3_bucket=${s3_bucket}
export FINANCE_SCRAPING_aws_profile=None
export FINANCE_SCRAPING_urls_s3_key=${urls_s3_key}
export FINANCE_SCRAPING_user_agent="${user_agent}"
export FINANCE_SCRAPING_max_retries=${max_retries}
export FINANCE_SCRAPING_backoff_factor=${backoff_factor}
export FINANCE_SCRAPING_retry_on=${retry_on}
export FINANCE_SCRAPING_timeout=${timeout}
export FINANCE_SCRAPING_host=${host}
export FINANCE_SCRAPING_port=${port}
export FINANCE_SCRAPING_db_username=${db_username}
export FINANCE_SCRAPING_db_password=${db_password}
export FINANCE_SCRAPING_db_name=${db_name}
export FINANCE_SCRAPING_db_table=${db_table}
EOL

cat << EOL >> $AIRFLOW_HOME/.bash_profile
export FINANCE_SCRAPING_dag_start_date=$(date -d "yesterday 22:00" -u -Iminutes)
export FINANCE_SCRAPING_s3_bucket=${s3_bucket}
export FINANCE_SCRAPING_aws_profile=None
export FINANCE_SCRAPING_urls_s3_key=${urls_s3_key}
export FINANCE_SCRAPING_user_agent="${user_agent}"
export FINANCE_SCRAPING_max_retries=${max_retries}
export FINANCE_SCRAPING_backoff_factor=${backoff_factor}
export FINANCE_SCRAPING_retry_on=${retry_on}
export FINANCE_SCRAPING_timeout=${timeout}
export FINANCE_SCRAPING_host=${host}
export FINANCE_SCRAPING_port=${port}
export FINANCE_SCRAPING_db_username=${db_username}
export FINANCE_SCRAPING_db_password=${db_password}
export FINANCE_SCRAPING_db_name=${db_name}
export FINANCE_SCRAPING_db_table=${db_table}
EOL

cat << EOL >> /etc/profile
export PATH=/usr/local/bin:$PATH
export AIRFLOW_HOME=/home/airflow
EOL

tree $AIRFLOW_HOME

pip3 install apache-airflow[systemd]

tree $AIRFLOW_HOME

chown -R airflow:airflow $AIRFLOW_HOME

#cat << EOL > $AIRFLOW_HOME/airflow.cfg
#{airflow_config}
#EOL

pip3 install finance-scraping

mkdir -p $AIRFLOW_HOME/dags

git clone https://github.com/jschnab/finance-scraping.git

mv finance-scraping $AIRFLOW_HOME/

cp $AIRFLOW_HOME/finance-scraping/finance_scraping/finance_scraping_dag.py $AIRFLOW_HOME/dags/

tree $AIRFLOW_HOME

airflow initdb

tree $AIRFLOW_HOME

chown -R airflow:airflow $AIRFLOW_HOME

systemctl enable airflow-webserver
systemctl enable airflow-scheduler
systemctl start airflow-webserver
systemctl start airflow-scheduler
