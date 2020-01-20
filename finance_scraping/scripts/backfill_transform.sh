#!/bin/bash

set -e

# this script backfills the transform step (parse HTML pages) from the finance-scraping
# ETL pipeline
# dates are inclusive and have to be in format YYYY-MM-DD
# use: bash backfill_transform.sh <start date> <end date>

START=$1
END=$(date -I -d "$2 + 1 day")

while [[ $START != $END ]]; do
    if [[ $(date +%u -d $START) -le 5 ]]; then
	echo "parsing web pages for $START"
	finance-scraper -t -d $START
    fi
    START=$(date -I -d "$START + 1 day")
done

echo "parsing done"
