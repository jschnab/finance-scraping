import csv
import numpy as np


def string_to_float(string):
    """
    Convert a string with a comma (i.e. '3.14') to a float.

    :param str string: string representing a float
    :return numpy.float:
    """
    # \xa0 is non-breaking space in latin1
    string_modif = string.replace(u',', u'.').replace(u'\xa0', u'')
    if string_modif == '':
        return np.nan
    else:
        return np.float(string_modif)


def parse_webpage(page_contents):
    """
    Parse the text of the HTML page.

    :param str page_contents: HTML code of the web page
    :return dict: dictionary where keys are stock attributes and values are
                  the corresponding values parsed from the HTML
    """
    results = {}

    parsed = BeautifulSoup(page_contents, 'html.parser')

    # get name of company
    results['company_name'] = content.find(
        'span',
        attrs={'class':'securityName'}
    )

    # get last_quote
    last_quote = content.find('span', attrs={'id':'Col0Price'})
    results['last_quote'] = string_to_float(last_quote)

    # get date
    timestamp = content.find('p', attrs={'id':'Col0PriceTime'}).split(' ')[1]
    results['last_time'] = timestamp[10:]
    last_date_raw = timestamp[:10]
    # if there is not date, set to 'NULL'
    last_date = re.sub(f'(\d+)/(\d+)/(\d+)', r'\3-\2-\1', last_date_raw)
    if last_date == last_date_raw:
        results['last_date'] = 'NULL'
    else:
        results['last_date'] = last_date

    # get last quote relative variation
    quote_detail = content.find('span', attrs={'id':'Col0PriceDetail'})
    quote_detail_abs = quote_detail.split('|')[0]
    results['quote_detail_abs'] = string_to_float(quote_detail_abs)
    quote_detail_rel = quote_detail.split('|')[1].replace('%', '')
    results['quote_detail_rel'] = string_to_float(quote_detail_rel) / 100

    # get bid and offer
    bid_offer = content.find('td', attrs={'id':'Col0BidOffer'}).split(' - ')
    results['bid'] = string_to_float(bid_offer[0])
    results['offer'] = string_to_float(bid_offer[1])

    # get daily low/high
    lo_hi = content.find('td', attrs={'id':'Col0LowHigh'}).split(' - ')
    if len(lo_hi) == 2:
        results['low'] = string_to_float(lo_hi[0])
        results['high'] = string_to_float(lo_hi[1])
    else:
        results['low'] = 'NULL'
        results['high'] = 'NULL'

    # get daily volume
    day_vol = content.find('td', attrs={'id':'Col0DayVolume'})
    results['daily_vol'] = string_to_float(day_vol)

    # capital
    capital_str = content.find('td', attrs={'id':'Col0MCap'})
    if capital_str[-3:] == 'Mil':
        capital = string_to_float(capital_str[:-3]) * 10e6
    elif capital_str[-3:] == 'Bil':
        capital = string_to_float(capital_str[:-3]) * 10e9
    else:
        capital = string_to_float(capital_str)
    results['capital'] = capital

    # get last closing value
    last_close = content.find('td', attrs={'id':'Col0LastClose'})
    results['last_close'] = string_to_float(last_close)

    # get yield ratio P/E
    p_e = content.find('td', attrs={'id':'Col0PE'})
    results['p_e'] = string_to_float(p_e)

    # get yield (percent)
    _yield = content.find('td', attrs={'id':'Col0Yield'})
    yield_percent = string_to_float(_yield) / 100
    results['yield_percent'] = yield_percent

    return results
