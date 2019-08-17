# script to perform web scraping of financial data
# see https://towardsdatascience.com/stock-market-analysis-in-python-part-1-getting-data-by-web-scraping-cb0589aca178 

import bs4
from bs4 import BeautifulSoup
from datetime import datetime
from io import StringIO
import numpy as np
import os
import requests

import boto3


def get_urls(urls_file):
    """
    Get the list of URLs to scrape from a text file.

    :param str urls_file: path to the file containing URLs
    :return list(str): list of URLs
    """
    with open(urls_file) as f:
        urls = f.readlines()

    urls_stripped = [u.strip('\n') for u in urls]

    return urls_stripped


def download_page_contents(session, url):
    """
    Download the contents of a web page.

    :param requests.Session: Session object
    :param str url: page URL
    :return bytes: web page contents
    """
    try:
        response = session.get(url, timeout=10)

    except:
        pass

    response.raise_on_status()

    return response.content


def upload_file_object_to_s3(file_object, bucket, key):
    """
    Upload a file-like object to S3.

    :param data: a file-like object such as a StringIO object
    :param str bucket: S3 bucket where to upload data
    :param str key: S3 object key where to upload data
    """
    client = boto3.client('s3')

    response = client.upload_fileobj(Body=file_object, Bucket=bucket, Key=key)

    check_response(response)


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
            # stay in the loop while the files contains lines with a URL
            if url != '':
                try:
                    response = requests.get(url, timeout=100)
                except ConnectionResetError as e:
                    with open('errorlog.txt', 'a') as errorlog:
                        errorlog.write(str(datetime.now())[:19] + ' ' + e + '\n')
                    print('Could not read URL : ' + url)
                    continue

                if response.status_code == 200:
                    content = BeautifulSoup(response.content, 'html.parser')

                    # get name of company
                    name = content.find('span', attrs={'class':'securityName'}).get_text()

                    # get last_quote
                    last_quote = content.find('span', attrs={'id':'Col0Price'}).get_text()
                    last_quote = string_to_float(last_quote)

                    # get date
                    last_date = content.find('p', attrs={'id':'Col0PriceTime'}).get_text().split(' ')[1]
                    last_time = last_date[10:]
                    last_date = last_date[:10].split('/')
                    last_date = '-'.join(reversed(last_date))
                    # if there is not date, set to 'NULL'
                    if last_date == '--':
                        last_date = 'NULL'

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

                # if response.status code is not 200
                else:
                    print('Status code {0} - could not retrieve data for:'.format(response.status_code))
                    print('{0}\n'.format(url))

            else:
                # exit loop at the end of the file containing URLs
                break

    # print progress on console
    print('Web scraping done')

    # check if the script ran without errors
    return 0

if __name__ == '__main__':
    scraping()
