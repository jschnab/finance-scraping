from unittest import TestCase
from unittest.mock import patch, call

from .. import src.scraping


class TestScraping(TestCase):

    def test_validate_urls(self):
        urls = ['http://mydomain.com', 'www.nicewebsite.org', 'badurl.net']
        validated = scraping.validated_urls(urls)
        self.assertEqual(validated, urls[:2])
