#!/bin/bash

coverage run --source finance_scraping -m unittest
coverage report -m
