from io import BytesIO, StringIO
import logging
import time
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
        level=logging.INFO
    )

    # get parameters
    params = config.get_config()
    bucket = params['AWS']['s3_bucket']
    profile = params['AWS']['profile']
    urls_key = params['SCRAPING']['urls_s3_key']
    user_agent = params['REQUESTS']['user_agent']
    timeout = params['REQUESTS']['timeout']
    max_retries = params['REQUESTS']['max_retries']

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

        text_buffer = StringIO(results)
        stock_id = scraping.get_stock_id(url)
        zip_archive.writestr(f'{stock_id}.txt', text_buffer.getvalue())
        time.sleep(0.5)

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


if __name__ == '__main__':
    extract()
