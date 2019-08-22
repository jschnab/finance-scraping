from io import BytesIO, StringIO
import logging
import time
from zipfile import ZIP_DEFLATED, ZipFile

import aws
import config
import parsing_html
import scraping


def setup():
    """
    Retrieve configuration parameters from 'config.ini' and
    setup logging.

    :return dict: configuration parameters
    """
    # setup logging
    fmt = '%(asctime)s %(levalname)s: %(message)s'

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
    user_agent,
    timeout,
    max_retries
):
    """
    Perform the extraction steps of webscraping:
        - download raw pages contents
        - zip data
        - upload zipped archive to AWS S3

    :param str bucket: AWS S3 bucket where data is stored
    :param str urls_key: AWS S3 key of the file storing the URLs to scrape
    :param str profile: AWS profile
    :param str user_agent: user agent to use for HTTP requests
    :param int timeout: timeout period (seconds) for HTTP requests
    :param int max_retries: maximum number of retries on HTTP request failure
    """
    # get list of urls to scrape
    urls_list = scraping.get_urls(
        bucket,
        urls_key,
        profile
    )

    session = scraping.get_session(params['REQUESTS'])

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
    archive_key = aws.get_s3_key('raw-page-content', 'archive.zip')
    msg = f'uploading pages contents to s3://{bucket}/{archive_key}'
    logging.info(msg)

    aws.upload_object_to_s3(
        zip_file_object.getvalue(),
        bucket,
        archive_key,
        profile
    )

    logging.info('scraping finished')


def transform(
    bucket,
    profile
):
    """
    Perform the transform steps of the pipeline:
        - download and unzip raw page archive from AWS S3
        - parse page contents to retrieve financial data
        - write data as a CSV file
        - upload CSV to S3

    :param str bucket: AWS S3 bucket where data is stored
    :param str profile: AWS profile
    """
    # download raw webpages contents
    archive_key = aws.get_s3_key('raw-page-content', 'archive.zip')

    logging.info(f'downloading raw pages {archive_key} from bucket {bucket}')

    raw_pages_zip = aws.download_s3_object(
        bucket,
        archive_key,
        profile
    )

    logging.info('reading raw pages archive')
    zip_data = BytesIO(raw_pages_zip)
    zip_obj = ZipFile(zip_data, 'r')

    # unzip and parse data
    for file_name in zip_obj.namelist():
        logging.info(f'parsing {file_name}')
        page_contents = zpi_obj.read(file_name).decode()
        parsed = parsing_html.parse_webpage(page_contents)
        csv_obj = StringIO()
        in_out.write_csv(csv_obj, header, parsed)
        csv_key = aws.get_s3_key('output', f'{file_name}.csv')

        logging.info(f'uploading file {csv_key} to bucket {bucket}')
        aws.upload_object_to_s3(
            csv_obj,
            bucket,
            key,
            profile
        )


def main():
    """
    Run the entire ETL pipeline.
    """

    params = setup()

    extract(
        params['AWS']['s3_bucket'],
        params['SCRAPING']['urls_s3_key'],
        params['AWS']['profile'],
        params['REQUESTS']['user_agent'],
        params['REQUESTS']['timeout'],
        params['REQUESTS']['max_retries']
    )

    transform(params['AWS']['bucket'], params['AWS']['profile'])

if __name__ == '__main__':
    main()
