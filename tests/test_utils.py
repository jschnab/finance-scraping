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

    def test_format_date_monday(self):
        expected = '2020/09/22'

        input_date = '21-09-2020'
        date = format_date(input_date)
        self.assertEqual(expected, date)

        input_date = '21 September 2020'
        date = format_date(input_date)
        self.assertEqual(expected, date)

        input_date = 'September, 21st 2020'
        date = format_date(input_date)
        self.assertEqual(expected, date)

    def test_format_date_friday(self):
        expected = '2020/09/21'

        input_date = '18-09-2020'
        date = format_date(input_date)
        self.assertEqual(expected, date)

        input_date = '18 September 2020'
        date = format_date(input_date)
        self.assertEqual(expected, date)

        input_date = 'September, 18th 2020'
        date = format_date(input_date)
        self.assertEqual(expected, date)
