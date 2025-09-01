#!/bin/bash

set -ex
set -o pipefail

exec > >(tee /var/log/user_data.log | logger -t user_data) 2>&1
echo BEGIN
BEGINTIME=$(date +%s)
date "+%Y-%m-%d %H:%M:%S"

yum update -y
yum install -y git python3 gcc postgresql-devel python3-devel.x86_64
amazon-linux-extras install -y epel nginx1

pip3 install gunicorn dash pandas

cd /home/ec2-user
git clone https://github.com/jschnab/finance-scraping.git
pip3 install finance-scraping/.

mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
cat << EOF > /etc/nginx/nginx.conf
${nginx_conf}
EOF

cat << EOF > /etc/systemd/system/gunicorn.service
${gunicorn_service}
EOF

cat << EOF > /etc/systemd/system/gunicorn.socket
${gunicorn_socket}
EOF

cat << EOF > /home/ec2-user/gunicorn.env
N_CORES=$((2 * $(grep -c processor /proc/cpuinfo) + 1))
FINANCE_SCRAPING_HOST=${host}
FINANCE_SCRAPING_PORT=${port}
FINANCE_SCRAPING_DB_USERNAME=${db_username}
FINANCE_SCRAPING_DB_PASSWORD=${db_password}
FINANCE_SCRAPING_DB_NAME=${db_name}
FINANCE_SCRAPING_DB_TABLE=${db_table}
EOF

systemctl enable --now gunicorn.socket
systemctl enable nginx
systemctl start nginx

date "+%Y-%m-%d %H:%M:%S"
ENDTIME=$(date +%s)
echo "Startup took $((ENDTIME - BEGINTIME)) seconds"
echo END
