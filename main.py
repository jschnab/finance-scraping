from io import BytesIO, StringIO
import logging
from zipfile import ZIP_DEFLATED, ZipFile

import aws
import config
import scraping


def extract():

    # setup logging
    fmt = '%(asctime)s %(message)s'

    logging.basicConfig(
        filename='log.txt',
        format=fmt,
        filemode='a',
        level=logging.DEBUG
    )

    # get parameters
    params = config.get_config()
    bucket = params['AWS']['s3_bucket']
    profile = params['AWS']['profile']
    urls_key = params['SCRAPING']['urls_s3_key']
    timeout = params['REQUESTS']['timeout']
    max_retries = params['REQUESTS']['max_retries']

    # get list of urls to scrape
    urls_list = scraping.get_urls(
        bucket,
        urls_key,
        profile
    )

    session = scraping.get_session(params['SESSION'])

    # open a ZipFile archive to be stored in memory
    zip_file_object = BytesIO()
    zip_archive = ZipFile(zip_file_object, 'a', compression=ZIP_DEFLATED)

    # iterate through URL and download page content
    logging.debug('scraping started')

    for url in urls_list:

        results = scraping.download_page_contents(
            session,
            url,
            timeout,
            max_retries
        )

        # if scraping of this page was successful
        if isinstance(results, str):
            text_buffer = StringIO(results)
            stock_id = scraping.get_stock_id(url)
            zip_archive.writestr(f'{stock_id}.txt', text_buffer.getvalue())

        # if the server responds with a code indicating failure
        elif isinstance(results, int):
            msg = f'scraping {url} failed with status code {results}'
            logging.debug(msg)

        # if too many connection errors happened
        elif isinstance(results, list):
            errors = ', '.join(results)
            msg = f'scraping {url} failed with the following errors: {errors}'
            logging.debug(msg)

    # upload ZIP archive containing raw page contents to S3
    archive_key = aws.get_s3_key('raw-page-content', 'archive.zip')
    msg = f'uploading pages contents to  s3://{bucket}/{archive_key}'
    logging.debug(msg)

    aws.upload_object_to_s3(
        zip_file_object.getvalue(),
        bucket,
        archive_key,
        profile
    )


if __name__ == '__main__':
    extract()
