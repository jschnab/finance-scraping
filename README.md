# Finance scraper

## Description

This repository contains a Extract-Transform-Load (ETL) pipeline which extracts security
data details from pages on [morningstar.fr](http://tools.morningstar.fr/fr/stockreport/default.aspx?Site=fr&id=0P0001A178&LanguageId=fr-FR&SecurityToken=0P0001A178]3]0]E0WWE$$ALL,DREXG$XHEL,DREXG$XLON,DREXG$XNYS). The step of the pipeline are:
* extract: scrape web pages and save them raw on AWS S3
* transform: parse raw web pages and store the results in a CSV file, store in S3
* load: copy the CSV file into a Postgres database

## How to run
### Requirements
* Python >= 3.6
* requests >= 2.22
* BeautifulSoup4 >= 4.7.1
* psycopg2 >= 2.8
* responses >= 0.10.6

### Installation
* Make sure you installed the correct version of Python and the required libraries.
* Clone this repository.
* Install Posgres, and create a database to load data into. Take note of the user name and
password with write privileges to this database.
* Go to the root folder of the repository and then run `python main.py -c` to set the
configuration of the scraper. You will be prompted to enter configuration values.
* Start the pipeline by running `python main.py -etl` to run the entire pipeline, or eitherof the optional arguments `-e`, `-t` or `-l` to run an individual step. It is possible to specify the date parameter `-d` with `-t` and/or `-l` to process data scraped on a specific
date. For more information run help with `python main.py -h`.