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
FINANCE_SCRAPING_DAG_START_DATE=$(date -d "yesterday 22:00" "+%Y-%m-%dT%H:%M")
FINANCE_SCRAPING_S3_BUCKET=${s3_bucket}
FINANCE_SCRAPING_AWS_PROFILE=None
FINANCE_SCRAPING_URLS_S3_KEY=${urls_s3_key}
FINANCE_SCRAPING_USER_AGENT="${user_agent}"
FINANCE_SCRAPING_MAX_RETRIES=${max_retries}
FINANCE_SCRAPING_BACKOFF_FACTOR=${backoff_factor}
FINANCE_SCRAPING_RETRY_ON=${retry_on}
FINANCE_SCRAPING_TIMEOUT=${timeout}
FINANCE_SCRAPING_HOST=${host}
FINANCE_SCRAPING_PORT=${port}
FINANCE_SCRAPING_DB_USERNAME=${db_username}
FINANCE_SCRAPING_DB_PASSWORD=${db_password}
FINANCE_SCRAPING_DB_NAME=${db_name}
FINANCE_SCRAPING_DB_TABLE=${db_table}
EOL

set -a
source $AIRFLOW_ENV
set +a

cat << EOL >> /etc/profile
export PATH=/usr/local/bin:$PATH
export AIRFLOW_HOME=/home/airflow
EOL

pip3 install apache-airflow[systemd]

cat << EOL > $AIRFLOW_HOME/airflow.cfg
${airflow_config}
EOL

pip3 install finance-scraping

mkdir -p $AIRFLOW_HOME/dags

git clone https://github.com/jschnab/finance-scraping.git

mv finance-scraping $AIRFLOW_HOME/

cp $AIRFLOW_HOME/finance-scraping/finance_scraping/finance_scraping_dag.py $AIRFLOW_HOME/dags/

airflow initdb

chown -R airflow:airflow $AIRFLOW_HOME

systemctl enable airflow-webserver
systemctl enable airflow-scheduler
systemctl start airflow-webserver
systemctl start airflow-scheduler
