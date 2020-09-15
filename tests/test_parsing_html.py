from bs4 import BeautifulSoup
from math import isnan
from unittest import TestCase
from unittest.mock import patch

from finance_scraping.parsing_html import (
    string_to_float,
    to_null,
    get_company_name,
    get_company_symbol,
    get_last_quote,
    get_date_time,
    get_daily_change,
    get_bid_offer,
    get_low_high,
    get_daily_volume,
    get_capital,
    get_closing_value,
    get_PE_ratio,
    get_yield,
    parse_webpage
)


class TestParsingHTML(TestCase):

    def test_string_to_float(self):
        string = u'\xa03.14'
        f = string_to_float(string)
        self.assertEqual(f, 3.14)

    def test_string_to_float_nan(self):
        f = string_to_float('')
        self.assertTrue(isnan(f))
        f = string_to_float('-')
        self.assertTrue(isnan(f))

    def test_to_null(self):
        d = {'key1': 'value1', 'key2': '', 'key3': float('nan')}
        expected = {'key1': 'value1', 'key2': 'NULL', 'key3': 'NULL'}
        d_to_null = to_null(d)
        self.assertEqual(d_to_null, expected)


class TestParsingHTMLBeautifulSoup(TestCase):
    def setUp(self):
        with open('webpage.txt') as f:
            self.page_contents = f.read()

        self.soup = BeautifulSoup(self.page_contents, 'html.parser')

    def test_get_company_name(self):
        name = get_company_name(self.soup)
        self.assertEqual(name, 'Acteos')

    def test_get_company_symbol(self):
        name = get_company_symbol(self.soup)
        self.assertEqual(name, 'EOS')

    def test_get_last_quote(self):
        quote = get_last_quote(self.soup)
        self.assertEqual(quote, 0.9)

    def test_get_date_time(self):
        time, date = get_date_time(self.soup)
        self.assertEqual(date, '2019-08-30')
        self.assertEqual(time, '16:38:37')

    def test_get_daily_change(self):
        absolute, relative = get_daily_change(self.soup)
        self.assertEqual(absolute, -0.01)
        self.assertAlmostEqual(relative, -0.0153)

    def test_get_bid_offer(self):
        bid, offer = get_bid_offer(self.soup)
        self.assertAlmostEqual(bid, 0.9)
        self.assertAlmostEqual(offer, 0.92)

    def test_get_low_high(self):
        low, high = get_low_high(self.soup)
        self.assertAlmostEqual(low, 0.9)
        self.assertAlmostEqual(high, 0.92)

    def test_get_daily_volume(self):
        volume = get_daily_volume(self.soup)
        self.assertAlmostEqual(volume, 878)

    def test_get_capital(self):
        capital = get_capital(self.soup)
        self.assertFalse(isnan(capital))

    def test_get_closing_value(self):
        last_close = get_closing_value(self.soup)
        self.assertAlmostEqual(last_close, 0.92)

    def test_get_PE_ratio(self):
        ratio = get_PE_ratio(self.soup)
        self.assertAlmostEqual(ratio, -5.97)

    def test_get_yield(self):
        y = get_yield(self.soup)
        self.assertTrue(isnan(y))

    @patch("finance_scraping.parsing_html.get_yield")
    @patch("finance_scraping.parsing_html.get_PE_ratio")
    @patch("finance_scraping.parsing_html.get_closing_value")
    @patch("finance_scraping.parsing_html.get_capital")
    @patch("finance_scraping.parsing_html.get_daily_volume")
    @patch("finance_scraping.parsing_html.get_low_high")
    @patch("finance_scraping.parsing_html.get_bid_offer")
    @patch("finance_scraping.parsing_html.get_daily_change")
    @patch("finance_scraping.parsing_html.get_date_time")
    @patch("finance_scraping.parsing_html.get_last_quote")
    @patch("finance_scraping.parsing_html.get_company_name")
    @patch("finance_scraping.parsing_html.BeautifulSoup")
    @patch("finance_scraping.parsing_html.to_null")
    def test_parse_webpage(
        self,
        to_null_mock,
        bs_mock,
        name_mock,
        last_quote_mock,
        date_time_mock,
        daily_change_mock,
        bid_offer_mock,
        low_high_mock,
        daily_volume_mock,
        capital_mock,
        closing_value_mock,
        PE_mock,
        yield_mock
    ):
        to_null_mock.return_value = 'results'
        bs_mock.return_value = 'soup'
        name_mock.return_value = 'name'
        last_quote_mock.return_value = 'last_quote'
        date_time_mock.return_value = 'time', 'date'
        daily_change_mock.return_value = 'abs', 'rel'
        bid_offer_mock.return_value = 'bid', 'offer'
        low_high_mock.return_value = 'low', 'high'
        daily_volume_mock.return_value = 'volume'
        capital_mock.return_value = 'capital'
        closing_value_mock.return_value = 'last_close'
        PE_mock.return_value = 'pe'
        yield_mock.return_value = 'yield'

        results = parse_webpage(self.page_contents, '2019-08-31', 'file.ext')

        self.assertEqual(results, 'results')
        bs_mock.assert_called_with(self.page_contents, 'html.parser')
        name_mock.assert_called_with('soup')
        last_quote_mock.assert_called_with('soup')
        date_time_mock.assert_called_with('soup')
        daily_change_mock.assert_called_with('soup')
        bid_offer_mock.assert_called_with('soup')
        low_high_mock.assert_called_with('soup')
        daily_volume_mock.assert_called_with('soup')
        capital_mock.assert_called_with('soup')
        closing_value_mock.assert_called_with('soup')
        PE_mock.assert_called_with('soup')
        yield_mock.assert_called_with('soup')
        to_null_mock.assert_called_once()
