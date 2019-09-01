from unittest import TestCase

from finance_scraping import config


class TestConfig(TestCase):

    def test_get_config(self):
        config_dict = {
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
                'user': 'username',
                'password': 'pa$$w0rd',
                'host': 'localhost',
                'port': '1234'
            }
        }
        c = config.ConfigParser()
        c['AWS'] = config_dict['AWS']
        c['SCRAPING'] = config_dict['SCRAPING']
        c['DATABASE'] = config_dict['DATABASE']
        expected = {
            'AWS': c['AWS'],
            'SCRAPING': c['SCRAPING'],
            'REQUESTS': config_dict['REQUESTS'],
            'DATABASE': c['DATABASE']
        }
        configuration = config.get_config()
        self.assertEqual(configuration, expected)
