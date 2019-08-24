import argparse
from dateutil import parser


def format_date(date):
    """
    Format a string representing a date into '%Y/%m/%d'.

    :param str date: date to format
    :return str: formatted date
    """
    date = parser.parse(date)
    return date.strftime('%Y/%m/%d')


def parse_cli():
    """
    Parse command-line interface arguments.

    :return: arguments
    """
    parser = argparse.ArgumentParser('Command-line interface for web scraper')

    parser.add_argument(
        '-c',
        '--configure',
        action='store_true',
        help='configure the scraper'
    )

    parser.add_argument(
        '-e',
        '--extract',
        action='store_true',
        help='run the extract step of the pipeline'
    )

    parser.add_argument(
        '-t',
        '--transform',
        action='store_true',
        help='run the transform step of the pipeline'
    )

    parser.add_argument(
        '-d',
        '--date',
        type=str,
        help='specify date of data collection for transform or load'
    )

    args = parser.parse_args()

    error_message = (
        "Do not specify options 'extract' and 'date' at the same time, "
        "'date' should only be specified when calling 'transform' and/or "
        "'load'."
    )
    assert not (args.extract and args.date), error_message

    return args
