import re

from bs4 import BeautifulSoup

import utils

# a way to check if a results is 'NaN'
NAN = float('nan')


def string_to_float(string):
    """
    Convert a string with a comma (i.e. '3.14') to a float.

    :param str string: string representing a float
    :return numpy.float:
    """
    # \xa0 is non-breaking space in latin1
    string_modif = string.replace(u',', u'.').replace(u'\xa0', u'')

    # empty strings or symbols (e.g. '-') would throw a ValueError
    try:
        return float(string_modif)
    except ValueError:
        return NAN


def to_null(d):
    """
    Converts the NaN (not a number) or empty values of a dictionary to the
    string 'NULL'.

    :param dict d: dictionary to convert
    :return dict: dictionary where NaN and empty values are 'NULL'
    """
    for key, value in d.items():
        if value is NAN or not value:
            d[key] = 'NULL'
    return d


def parse_webpage(page_contents, collection_date):
    """
    Parse the text of the HTML page.

    :param str page_contents: HTML code of the web page
    :param str collection_date: date when data was collected
    :return dict: dictionary where keys are stock attributes and values are
                  the corresponding values parsed from the HTML
    """
    if not collection_date:
        collection_date = utils.format_date(collection_date)

    results = {'collection_date': collection_date}

    soup = BeautifulSoup(page_contents, 'html.parser')

    # get name of company
    results['company_name'] = soup.find(
        'span',
        attrs={'class': 'securityName'}
    ).get_text()

    # get last_quote
    last_quote = soup.find('span', attrs={'id': 'Col0Price'}).get_text()
    results['last_quote'] = string_to_float(last_quote)

    # get date and time
    timestamp = soup.find(
        'p',
        attrs={'id': 'Col0PriceTime'}
    ).get_text().split()[1]
    results['time'] = timestamp[10:]
    date_raw = timestamp[:10]

    # if there is not date, set to 'NULL'
    date = re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\2-\1', date_raw)
    if date == date_raw:
        results['date'] = 'NULL'
    else:
        results['date'] = date

    # get last quote relative variation
    quote_detail = soup.find(
        'span',
        attrs={'id': 'Col0PriceDetail'}
    ).get_text()

    quote_detail_abs = quote_detail.split('|')[0]
    results['daily_change_abs'] = string_to_float(quote_detail_abs)
    quote_detail_rel = quote_detail.split('|')[1].replace('%', '')
    quote_detail_rel = string_to_float(quote_detail_rel)
    # NAN / 100 is not NAN
    if quote_detail_rel is NAN:
        results['daily_change_rel'] = quote_detail_rel
    else:
        results['daily_change_rel'] = quote_detail_rel / 100

    # get bid and offer
    bid_offer = soup.find(
        'td',
        attrs={'id': 'Col0BidOffer'}
    ).get_text().split(' - ')

    results['bid'] = string_to_float(bid_offer[0])
    results['offer'] = string_to_float(bid_offer[1])

    # get daily low/high
    lo_hi = soup.find(
        'td',
        attrs={'id': 'Col0LowHigh'}
    ).get_text().split(' - ')

    if len(lo_hi) == 2:
        results['low'] = string_to_float(lo_hi[0])
        results['high'] = string_to_float(lo_hi[1])
    else:
        results['low'] = 'NULL'
        results['high'] = 'NULL'

    # get daily volume
    day_vol = soup.find('td', attrs={'id': 'Col0DayVolume'}).get_text()
    results['day_volume'] = string_to_float(day_vol)

    # capital
    capital_str = soup.find('td', attrs={'id': 'Col0MCap'}).get_text()
    if capital_str[-3:] == 'Mil':
        capital = string_to_float(capital_str[:-3]) * 10e6
    elif capital_str[-3:] == 'Bil':
        capital = string_to_float(capital_str[:-3]) * 10e9
    else:
        capital = string_to_float(capital_str)
    results['capital'] = capital

    # get last closing value
    last_close = soup.find('td', attrs={'id': 'Col0LastClose'}).get_text()
    results['last_close'] = string_to_float(last_close)

    # get yield ratio P/E
    p_e = soup.find('td', attrs={'id': 'Col0PE'}).get_text()
    results['p_e'] = string_to_float(p_e)

    # get yield (percent)
    _yield = soup.find('td', attrs={'id': 'Col0Yield'}).get_text()
    _yield = string_to_float(_yield)
    results['yield_percent'] = _yield if _yield is NAN else _yield / 100

    # convert all NaN to 'NULL'
    results = nan_to_null(results)

    return results
