from unittest import TestCase
from unittest.mock import patch

from finance_scraping.scraping import (
    validate_urls,
    get_urls,
    get_session,
    download_page_contents,
    get_security_id
)


class SessionMock:
    """Class to fake a requests.Session object."""
    def __init__(self, ok, text):
        self.ok = ok
        self.text = text

    def get(self, url, timeout, headers):
        if url == 'bad_url':
            raise ValueError
        return ResponseMock(self.ok, self.text)


class ResponseMock:
    """Class to fake a requests.Session object."""
    def __init__(self, ok, text):
        self.ok = ok
        self.text = text
        self.status_code = 404


class TestScraping(TestCase):

    def test_validate_urls(self):
        urls = ['http://mydomain.com', 'www.nicewebsite.org', 'badurl.net']
        validated = validate_urls(urls)
        expected = ['http://mydomain.com', 'http://www.nicewebsite.org']
        self.assertEqual(validated, expected)

    @patch("finance_scraping.aws.download_s3_object")
    def test_get_urls(self, download_mock):
        download_mock.return_value = \
                b'www.mysite.com\nthis is not a url\nhttp://www.visitme.fr\n'
        validated = get_urls('bucket', 'key', 'profile')
        expected = ['http://www.mysite.com', 'http://www.visitme.fr']
        self.assertEqual(validated, expected)

    @patch("finance_scraping.scraping.Retry")
    @patch("finance_scraping.scraping.requests.Session")
    def test_get_session(self, session_mock, retry_mock):
        _ = get_session(10, 0.3, [500, 502, 504])
        retry_mock.assert_called_with(
            total=10,
            read=10,
            connect=10,
            backoff_factor=0.3,
            status_forcelist=[500, 502, 504]
        )

    def test_download_page_contents(self):
        session = SessionMock(ok=True, text='hello')
        text = download_page_contents(
            session,
            'url',
            'timeout',
            'headers',
            10
        )
        self.assertEqual(text, 'hello')

    @patch("finance_scraping.scraping.logging")
    @patch("finance_scraping.scraping.time")
    def test_download_page_contents_error(self, time_mock, log_mock):
        session = SessionMock(ok=True, text='hello')
        _ = download_page_contents(
            session,
            'bad_url',
            'timeout',
            'headers',
            10
        )
        time_mock.sleep.assert_called_with(10)
        log_mock.error.assert_called_with('scraping failed:  for bad_url')

    @patch("finance_scraping.scraping.logging")
    @patch("finance_scraping.scraping.time")
    def test_download_page_bad_status_code(self, time_mock, log_mock):
        session = SessionMock(ok=False, text='hello')
        _ = download_page_contents(
            session,
            'url',
            'timeout',
            'headers',
            10
        )
        log_mock.error.assert_called_with('scraping failed: 404 for url')

    def test_get_security_id(self):
        url = (
            'http://tools.morningstar.fr/fr/stockreport/default.aspx?Site=fr'
            '&id=0P0001DIM8&LanguageId=fr-FR&SecurityToken=0P0001DIM8]3]0]E0W'
            'WE$$ALL,DREXG$XHEL,DREXG$XLON,DREXG$XNYS'
        )
        security_id = get_security_id(url)
        self.assertEqual(security_id, '0P0001DIM8')
