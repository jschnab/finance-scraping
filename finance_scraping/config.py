import os
from os.path import dirname, join
import subprocess


def get_environment_variables():
    """
    Read the configuration from the environment variables.

    :return dict[dict]: configuration
    """
    configuration = {}

    configuration['AWS'] = {
        's3_bucket': os.getenv('FINANCE_SCRAPING_S3_BUCKET'),
        'profile': os.getenv('FINANCE_SCRAPING_AWS_PROFILE')
    }
    # set AWS profile to None if user typed 'None'
    if configuration['AWS']['profile'] == 'None':
        configuration['AWS']['profile'] = None

    configuration['REQUESTS'] = {
        'user_agent': os.getenv('FINANCE_SCRAPING_USER_AGENT'),
        'max_retries': int(os.getenv('FINANCE_SCRAPING_MAX_RETRIES')),
        'backoff_factor': float(os.getenv('FINANCE_SCRAPING_BACKOFF_FACTOR')),
        'retry_on': tuple(
            map(int, os.getenv('FINANCE_SCRAPING_RETRY_ON').split(','))),
        'timeout': int(os.getenv('FINANCE_SCRAPING_TIMEOUT'))
    }

    configuration['SCRAPING'] = {
        'urls_s3_key': os.getenv('FINANCE_SCRAPING_URLS_S3_KEY')}

    configuration['DATABASE'] = {
        'database': os.getenv('FINANCE_SCRAPING_DATABASE'),
        'table': os.getenv('FINANCE_SCRAPING_TABLE'),
        'db_user': os.getenv('FINANCE_SCRAPING_DB_USER'),
        'password': os.getenv('FINANCE_SCRAPING_PASSWORD'),
        'host': os.getenv('FINANCE_SCRAPING_HOST'),
        'port': os.getenv('FINANCE_SCRAPING_PORT'),
    }

    return configuration


def configure():
    """
    Run BASH configuration script.
    """
    config_file_path = join(
        dirname(__file__),
        join('scripts', 'configure.sh')
    )
    try:
        subprocess.run(['bash', config_file_path])
    # ProcessLookupError happens if you hit ctrl+c
    except (KeyboardInterrupt, ProcessLookupError):
        msg = (
            "\nConfiguration may be incomplete, "
            "run 'finance-scraping -c' again."
        )
        print(msg)


def terraform_configure():
    """
    Run BASH configuration script to store Terraform environment variables.
    """
    config_file_path = join(
        dirname(__file__),
        join('scripts', 'terraform_configure.sh')
    )
    try:
        subprocess.run(['bash', config_file_path])
    except (KeyboardInterrupt, ProcessLookupError):
        msg = (
            "\nConfiguration may be incomplete, "
            "run 'finance-scraping -c' again."
        )
        print(msg)
