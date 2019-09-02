#!/bin/bash

# get configuration from user's input and save it as environment variables

declare -a parameters=(s3_bucket aws_profile urls_s3_key user_agent \
    max_retries backoff_factor retry_on timeout database table user \
    password host port)

echo "Please enter configuration values: "
echo

# loop through parameters
for ((i=0; i<${#parameters[@]}; i++)); do

    # show the existing value to the user
    var="FINANCE_SCRAPING_${parameters[i]^^}"
    echo "${parameters[i]}[$(eval echo \$$var)]: "
    read val

    # keep waiting for user input if no value is set
    while [[ -z ${val} ]] && [[ -z $(eval echo \$$var) ]]; do
	echo "${parameters[i]}["$(eval echo \$$var)"]: "
	read val
    done

    # user's input overwrites the existing variable
    if [[ ! -z ${val} ]]; then
        export $var=$val
    fi
done
