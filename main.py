import csv
from datetime import datetime
from io import BytesIO, StringIO
import logging
import sys
import time
from zipfile import ZIP_DEFLATED, ZipFile

import aws
import config
import parsing_html
import scraping
import utils

RAW_PAGES_S3_PREFIX = 'raw-page-content'
RAW_PAGES_S3_SUFFIX = 'archive.zip'
SECURITY_REPORT_S3_PREFIX = 'parsed-page-data'
SECURITY_REPORT_S3_SUFFIX = 'security_report.csv'
CSV_HEADER = [
    'company_name',
    'capital',
    'date',
    'time',
    'last_quote',
    'last_close',
    'daily_change_abs',
    'daily_change_rel',
    'bid',
    'offer',
    'low',
    'high',
    'day_volume',
    'p_e',
    'yield_percent',
    'collection_date'
]


def setup():
    """
    Retrieve configuration parameters from 'config.ini' and
    setup logging.

    :return dict: configuration parameters
    """
    # setup logging
    fmt = '%(asctime)s %(levelname)s: %(message)s'

    logging.basicConfig(
        filename='log.txt',
        format=fmt,
        filemode='a',
        level=logging.INFO
    )

    # get parameters
    params = config.get_config()
    return params


def extract(
    bucket,
    urls_key,
    profile,
    max_retries,
    backoff_factor,
    retry_on,
    user_agent,
    timeout
):
    """
    Perform the extraction steps of webscraping:
        - download raw pages contents
        - zip data
        - upload zipped archive to AWS S3

    :param str bucket: AWS S3 bucket where data is stored
    :param str urls_key: AWS S3 key of the file storing the URLs to scrape
    :param str profile: AWS profile
    :param int max_retries: maximum number of retries on HTTP request failure
    :param float backoff_factor: delay backoff factor for HTTP request retries
    :param list(int) retry_on: HTTP status codes allowing HTTP request retry
    :param str user_agent: user agent to use for HTTP requests
    :param int timeout: timeout period (seconds) for HTTP requests
    """
    # get list of urls to scrape
    urls_list = scraping.get_urls(
        bucket,
        urls_key,
        profile
    )

    session = scraping.get_session(
        max_retries,
        backoff_factor,
        retry_on
    )

    # open a ZipFile archive to be stored in memory
    zip_file_object = BytesIO()
    zip_archive = ZipFile(zip_file_object, 'a', compression=ZIP_DEFLATED)

    # iterate through URL and download page content
    logging.info('scraping started')

    for url in urls_list:

        results = scraping.download_page_contents(
            session,
            url,
            user_agent,
            timeout,
            max_retries
        )

        # zip each page as a text file in an archive
        text_buffer = StringIO(results)
        stock_id = scraping.get_stock_id(url)
        zip_archive.writestr(f'{stock_id}.txt', text_buffer.getvalue())
        time.sleep(0.5)

    zip_archive.close()

    # upload ZIP archive containing raw page contents to S3
    date = datetime.today().strftime('%Y/%m/%d')
    archive_key = aws.get_s3_key(
        RAW_PAGES_S3_PREFIX,
        RAW_PAGES_S3_SUFFIX,
        date
    )
    msg = f'uploading pages contents to s3://{bucket}/{archive_key}'
    logging.info(msg)

    aws.upload_object_to_s3(
        zip_file_object,
        bucket,
        archive_key,
        profile
    )

    logging.info('scraping finished')


def transform(bucket, profile, date=None):
    """
    Perform the transform steps of the pipeline:
        - download and unzip raw page archive from AWS S3
        - parse page contents to retrieve financial data
        - write data as a CSV file
        - upload CSV to S3

    If you want to transform data collected at a date other than today,
    pass the 'date' argument.

    :param str bucket: AWS S3 bucket where data is stored
    :param str profile: AWS profile
    :param str date: date corresponding to the data to process,
                     optional (default None)
    """
    if not date:
        date = datetime.today().strftime('%Y/%m/%d')
    else:
        date = utils.format_date(date)

    # download raw web pages contents
    archive_key = aws.get_s3_key(
        RAW_PAGES_S3_PREFIX,
        RAW_PAGES_S3_SUFFIX,
        date
    )

    logging.info(f'downloading raw pages {archive_key} from bucket {bucket}')

    raw_pages_zip = aws.download_s3_object(
        bucket,
        archive_key,
        profile
    )

    # we will unzip web pages contents in memory
    logging.info('reading raw pages archive')
    zip_data = BytesIO(raw_pages_zip)
    zip_obj = ZipFile(zip_data, 'r')

    # we will write data parsed from the web page to a csv in memory
    # 1 page = 1 row
    csv_obj = StringIO()
    writer = csv.DictWriter(csv_obj, CSV_HEADER, lineterminator='\n')
    writer.writeheader()

    # loop through files in the archive (1 file = 1 web page)
    for file_name in zip_obj.namelist():

        logging.info(f'parsing {file_name}')

        # extract file content, parse HTML code, write to csv
        page_contents = zip_obj.read(file_name).decode()
        parsed = parsing_html.parse_webpage(page_contents, date)
        writer.writerow(parsed)

    csv_key = aws.get_s3_key(
        SECURITY_REPORT_S3_PREFIX,
        SECURITY_REPORT_S3_SUFFIX,
        date
    )

    logging.info(f'uploading file {csv_key} to bucket {bucket}')

    aws.upload_object_to_s3(
        csv_obj,
        bucket,
        csv_key,
        profile
    )


def main():
    """
    Run the entire ETL pipeline.
    """
    args = utils.parse_cli()
    print(args)
    sys.exit()

    if args.configure:
        config.configure()

    params = setup()

    if args.extract:
        extract(
            params['AWS']['s3_bucket'],
            params['SCRAPING']['urls_s3_key'],
            params['AWS']['profile'],
            params['REQUESTS']['max_retries'],
            params['REQUESTS']['backoff_factor'],
            params['REQUESTS']['retry_on'],
            params['REQUESTS']['user_agent'],
            params['REQUESTS']['timeout'],
        )

    if args.transform:
        transform(
            params['AWS']['s3_bucket'],
            params['AWS']['profile'],
            args.date
        )


if __name__ == '__main__':
    main()
