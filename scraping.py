# script to perform web scraping of financial data
# see https://towardsdatascience.com/stock-market-analysis-in-python-part-1-getting-data-by-web-scraping-cb0589aca178 

from datetime import datetime
import numpy as np
import requests
from bs4 import BeautifulSoup
import bs4
import os

# convert string with comma to float, e.g. '2,42' to 2.42
def string_to_float(string):
    """Convert a string with a comma to a float"""
    # \xa0 is non-breaking space in latin1
    string_modif = string.replace(u',', u'.').replace(u'-', u'').replace(u'\xa0', u'')
    if string_modif == '':
        return np.nan
    else:
        return np.float(string_modif)

def scraping():
    """Perform webscraping of financial data."""
    # get information from different companies
    # read URLs from text file, then get HTML page contents and add them in a pandas dataframe

    # get date, used as suffix for csv file
    today = datetime.now().strftime('%Y%m%d')

    # display progress on console
    print('Web scraping of financial data\n')

    # create a csv file with just header, to be appended with data below
    filename = '/home/jonathans/finance-scraping/finance-data-' + today + '.csv'
    with open(filename, 'w') as csvfile:
        csvfile.write('name,capital,date,time,lastquote,lastabs,lastrel,bid,offer,low,\
high,dayvol,pe,yield\n')

    # display progress on console
    print('Saving data in ' + filename + '\n')

    # read URLs from txt file
    links = '/home/jonathans/finance-scraping/scraping_links.txt'
    print('Scraping data from URLs stored in ' + links)
    print('Please wait, this may take a while...\n')
    with open(links, 'r') as urlfile:
        while True:
            url = urlfile.readline()
            if url != '':
                response = requests.get(url, timeout=240)
                content = BeautifulSoup(response.content, 'html.parser')

                # get name of company
                name = content.find('span', attrs={'class':'securityName'}).get_text()

                # get last_quote and date
                last_quote = content.find('span', attrs={'id':'Col0Price'}).get_text()
                last_quote = string_to_float(last_quote)
                last_date = content.find('p', attrs={'id':'Col0PriceTime'}).get_text().split(' ')[1]
                last_time = last_date[10:]
                last_date = last_date[:10]

                # get last quote relative variation
                quote_detail = content.find('span', attrs={'id':'Col0PriceDetail'}).get_text()
                quote_detail_abs = string_to_float(quote_detail.split('|')[0])
                quote_detail_rel = string_to_float(quote_detail.split('|')[1].replace('%', '')) / 100

                # get bid and offer
                bid_offer = content.find('td', attrs={'id':'Col0BidOffer'}).get_text().split(' - ')
                bid = string_to_float(bid_offer[0])
                offer = string_to_float(bid_offer[1])

                # get daily low/high
                lo_hi = content.find('td', attrs={'id':'Col0LowHigh'}).get_text().split(' - ')
                if len(lo_hi) == 2:
                    low = string_to_float(lo_hi[0])
                    high = string_to_float(lo_hi[1])
                else:
                    low = 'NULL'
                    high = 'NULL'

                # get daily volume
                day_vol = string_to_float(content.find('td', attrs={'id':'Col0DayVolume'}).get_text())

                # capital
                capital_str = content.find('td', attrs={'id':'Col0MCap'}).get_text()
                if capital_str[-3:] == 'Mil':
                    capital = string_to_float(capital_str[:-3]) * 10e6
                elif capital_str[-3:] == 'Bil':
                    capital = string_to_float(capital_str[:-3]) * 10e9
                else:
                    capital = string_to_float(capital_str)

                # get last closing value
                last_close = string_to_float(content.find('td', attrs={'id':'Col0LastClose'}).get_text())

                # get yield ratio P/E
                p_e = string_to_float(content.find('td', attrs={'id':'Col0PE'}).get_text())

                # get yield (percent)
                yield_percent = string_to_float(content.find('td', attrs={'id':'Col0Yield'}).get_text()) / 100

                # append data to a csv file
                writestring = ','.join([name, str(capital), last_date, last_time, str(last_quote),\
        str(quote_detail_abs), str(quote_detail_rel), str(bid), str(offer), str(low), str(high),\
        str(day_vol), str(p_e), str(yield_percent)])
                with open(filename, 'a') as csvfile:
                    csvfile.write(writestring + '\n')

            else:
                break

    # print progress on console
    print('Web scraping done')

    # check if the script ran without errors
    return 0

if __name__ == '__main__':
    scraping()
