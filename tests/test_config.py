import os
from unittest import TestCase

from finance_scraping import config


class TestConfig(TestCase):

    def setUp(self):
        self.config_dict = {
            'AWS': {
                's3_bucket': 'bucket',
                'profile': 'aws_profile'
            },
            'SCRAPING': {'urls_s3_key': 'urls.txt'},
            'REQUESTS': {
                'user_agent': 'my own scraper',
                'max_retries': 10,
                'backoff_factor': 0.3,
                'retry_on': (500, 502, 504),
                'timeout': 20
            },
            'DATABASE': {
                'database': 'scraping_db',
                'table': 'mytable',
                'db_user': 'username',
                'password': 'pa$$w0rd',
                'host': 'localhost',
                'port': '1234'
            }
        }

    def test_get_config(self):
        c = config.ConfigParser()
        c['AWS'] = self.config_dict['AWS']
        c['SCRAPING'] = self.config_dict['SCRAPING']
        c['DATABASE'] = self.config_dict['DATABASE']
        expected = {
            'AWS': c['AWS'],
            'SCRAPING': c['SCRAPING'],
            'REQUESTS': self.config_dict['REQUESTS'],
            'DATABASE': c['DATABASE']
        }
        configuration = config.get_config()
        self.assertEqual(configuration, expected)

    def test_get_environment_variables(self):
        prefix = 'FINANCE_SCRAPING_'
        os.environ[f'{prefix}S3_BUCKET'] = 'bucket'
        os.environ[f'{prefix}AWS_PROFILE'] = 'aws_profile'
        os.environ[f'{prefix}USER_AGENT'] = 'my own scraper'
        os.environ[f'{prefix}MAX_RETRIES'] = '10'
        os.environ[f'{prefix}BACKOFF_FACTOR'] = '0.3'
        os.environ[f'{prefix}RETRY_ON'] = '500,502,504'
        os.environ[f'{prefix}TIMEOUT'] = '20'
        os.environ[f'{prefix}URLS_S3_KEY'] = 'urls.txt'
        os.environ[f'{prefix}DATABASE'] = 'scraping_db'
        os.environ[f'{prefix}TABLE'] = 'mytable'
        os.environ[f'{prefix}DB_USER'] = 'username'
        os.environ[f'{prefix}PASSWORD'] = 'pa$$w0rd'
        os.environ[f'{prefix}HOST'] = 'localhost'
        os.environ[f'{prefix}PORT'] = '1234'
        configuration = config.get_environment_variables()
        self.assertEqual(self.config_dict, configuration)
