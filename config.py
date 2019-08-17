from configparser import ConfigParser


def get_config():
    """
    Read configuration file and return the whole configuration.
    """
    config = ConfigParser()

    config.read('config.ini')

    return config


def get_session_parameters():
    """
    Get parameters for the the requests.Session object.

    :return dict: session parameters
    """
    config = get_config()['SCRAPING']

    session_params = {}

    session_params['max_retries'] = int(config['max_retries'])

    session_params['backoff_factor'] = float(config['backoff_factor'])

    session_params['retry_on'] = tuple(map(int, config['retry_on'].split(',')))

    session_params['timeout'] = int(config['timeout'])

    return session_params
