from dateutil import parser


def format_date(date):
    """
    Format a string representing a date into '%Y/%m/%d'.

    :param str date: date to format
    :return str: formatted date
    """
    date = parser.parse(date)
    return date.strftime('%Y/%m/%d')
