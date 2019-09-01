from unittest import TestCase

from finance_scraping.utils import (
    remove_header,
    format_date
)


class TestUtils(TestCase):

    def test_remove_header(self):
        text = "first line\nthis is the second line\nthird line\n"
        expected = "this is the second line\nthird line\n"
        no_header = remove_header(text, separator='\n')
        self.assertEqual(no_header, expected)

    def test_format_date(self):
        expected = '2019/08/31'

        input_date = '31-08-2019'
        date = format_date(input_date)
        self.assertEqual(expected, date)

        input_date = '31 August 2019'
        date = format_date(input_date)
        self.assertEqual(expected, date)

        input_date = 'August, 31st 2019'
        date = format_date(input_date)
        self.assertEqual(expected, date)
