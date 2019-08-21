from configparser import ConfigParser


def get_config():
    """
    Read configuration file, perform appropriate typ conversion
    and return the whole configuration.

    :return dict[dict]: configuration
    """
    config = ConfigParser()
    config.read('config.ini')

    # get AWS config
    aws_config = config['AWS']
    aws_params = {}
    aws_params['s3_bucket'] = aws_config['s3_bucket']
    aws_params['profile'] = aws_config['profile']

    # get requests config
    requests_config = config['REQUESTS']
    requests_params = {}
    requests_params['user_agent'] = requests_config['user_agent']
    requests_params['max_retries'] = int(requests_config['max_retries'])
    requests_params['backoff_factor'] = float(
        requests_config['backoff_factor']
    )

    requests_params['retry_on'] = tuple(
        map(int, requests_config['retry_on'].split(','))
    )

    requests_params['timeout'] = int(requests_config['timeout'])

    # get scraping config
    scraping_config = config['SCRAPING']
    scraping_params = {}
    scraping_params['urls_s3_key'] = scraping_config['urls_s3_key']

    return {
        'AWS': aws_params,
        'REQUESTS': requests_params,
        'SCRAPING': scraping_params
    }
