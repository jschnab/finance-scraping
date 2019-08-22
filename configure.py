#!/usr/bin/env python3

from configparser import ConfigParser

# get config
config = ConfigParser()
config.read('config.ini')

print('Please enter configuration values:\n')

for key in config.keys():

    for k, v in config[key].items():
        # we show the user the default value
        i = input(f'{k} [{v}]: ')

        # we wait for user input if no value is set (default or user input)
        while not v and not i:
            i = input(f'{k} [{v}]: ')

        # the eventual user input overwrites the default value
        if i:
            config[key][k] = i

with open('config.ini', 'w') as config_file:
    config.write(config_file)
